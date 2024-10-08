import json
import os
import random
import re
import asyncio
import tempfile
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote_plus

from anthropic import AsyncAnthropicBedrock, RateLimitError
from tqdm.auto import tqdm
from sklearn.metrics.pairwise import (
    cosine_similarity,
)
from sklearn.cluster import MeanShift
import numpy as np
import polars as pl
import s3fs

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.retrievers import BaseRetriever, RecursiveRetriever
from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.bedrock import BedrockEmbedding
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock import Bedrock
from llama_index.core.schema import TransformComponent, IndexNode, TextNode, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser

from dataset_tools.parsing.structured import VALUE_VALID_TEMPLATE, Column


from dataset_tools.cds.models import (
    CDS_COLUMNS,
)

from dataset_tools.parsing.structured import (
    EXTRACT_INFO_TEMPLATE,
    EXTRACT_KEY_VALUES_TEMPLATE,
    Column,
    columns_to_schema,
)

EMBED_MODEL: Optional[BedrockEmbedding] = None
# LLM: Optional[Bedrock] = None
client = AsyncAnthropicBedrock()
sem = asyncio.Semaphore(4)

dataframes_bucket = os.getenv(
    "DATAFRAMES_BUCKET", "s3://collega-dataframes-533267152364"
)


def setup():
    global EMBED_MODEL
    # global LLM

    EMBED_MODEL = BedrockEmbedding(model_name="cohere.embed-english-v3")
    # LLM = Bedrock(model="anthropic.claude-3-haiku-20240307-v1:0")


async def chat(prompt: str):
    timeout_sec = 1
    retries_remaining = 5

    async with sem:
        while retries_remaining >= 0:
            try:
                message = await client.messages.create(
                    # model="anthropic.claude-3-5-sonnet-20240620-v1:0",
                    model="anthropic.claude-3-haiku-20240307-v1:0",
                    max_tokens=2048,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                )

                return message.content[0].text
            except RateLimitError as e:
                retries_remaining -= 1

                if retries_remaining <= 0:
                    raise e
                else:
                    print(
                        f"Rate limit hit ({retries_remaining} tries remaining), retrying in {timeout_sec} seconds"
                    )

                    await asyncio.sleep(timeout_sec)
                    timeout_sec *= random.randint(2, 4)
                    continue


class KVPairExtractor(TransformComponent):
    async def acall(self, nodes, **kwargs):
        kv_pair_nodes = []

        async def extract_kv_pairs(node: BaseNode):
            key_values = await chat(EXTRACT_KEY_VALUES_TEMPLATE.format(text=node.text))

            lines = [line for line in key_values.splitlines() if len(line) > 0]

            for line in lines:
                text_node = TextNode(text=line)

                if line.startswith("*"):
                    index_node = IndexNode.from_text_node(text_node, node.node_id)
                    kv_pair_nodes.append(index_node)

            # Add back original node to list of nodes
            kv_pair_nodes.append(IndexNode.from_text_node(node, node.node_id))

        coros = []

        for node in nodes:
            # key_values_fut = LLM.achat(
            #     messages=[
            #         ChatMessage(
            #             role="user",
            #             content=EXTRACT_KEY_VALUES_TEMPLATE.format(text=node.text),
            #         )
            #     ],
            # )
            key_values_fut = extract_kv_pairs(node)
            coros.append(key_values_fut)

        if "show_progress" in kwargs and kwargs["show_progress"]:
            key_values_fut_gen = tqdm(
                asyncio.as_completed(coros), desc="Reformatting Nodes", total=len(coros)
            )
        else:
            key_values_fut_gen = asyncio.as_completed(coros)

        for key_values_fut in key_values_fut_gen:
            await key_values_fut

        return kv_pair_nodes

    def __call__(self, nodes, **kwargs):
        loop = asyncio.get_event_loop()

        nodes = loop.run_until_complete(self.acall(nodes, **kwargs))
        loop.close()

        return nodes


# def get_tqdm_iterable(items: Iterable, show_progress: bool, desc: str) -> Iterable:
#     """
#     Optionally get a tqdm iterable. Ensures tqdm.auto is used.
#     """
#     _iterator = items
#     if show_progress:
#         try:
#             from tqdm.auto import tqdm

#             return tqdm(items, desc=desc)
#         except ImportError:
#             pass
#     return _iterator


async def file_to_nodes(input_file: str):
    reader = SimpleDirectoryReader(
        input_files=[input_file],
    )

    documents = reader.load_data()

    pipeline = IngestionPipeline(
        transformations=[MarkdownNodeParser(), KVPairExtractor()],
        # transformations=[MarkdownNodeParser()],
    )

    return await pipeline.arun(documents=documents, show_progress=True)


async def get_target_column_names(
    text: str,
    columns: List[Column],
    column_embeddings: List[float],
    threshold: float,
):
    text_embedding = await EMBED_MODEL.aget_text_embedding(text=text)

    cosine_sims = cosine_similarity([text_embedding], column_embeddings)

    max_idx = np.argmax(cosine_sims, axis=1)[0]
    clustering = MeanShift().fit(cosine_sims[0].reshape(-1, 1))

    max_label = clustering.labels_[max_idx]

    found_columns = [
        column
        for i, column in enumerate(columns)
        if clustering.labels_[i] == max_label and cosine_sims[0][i] >= threshold
    ]

    return found_columns


async def get_column_json(text: str, columns: List[Column]):
    if columns == []:
        return None

    schema = columns_to_schema(columns)

    template_str = EXTRACT_INFO_TEMPLATE.format(text=text, schema=json.dumps(schema))
    # template_str = EXTRACT_INFO_TEMPLATE.format(text=text)

    attempts_remaining = 3

    while attempts_remaining > 0:
        # out = await LLM.achat(
        #     messages=[ChatMessage(role="user", content=template_str)],
        # )
        out = await chat(template_str)

        first_idx = out.find("{")
        last_idx = out.rfind("}")

        # json_regex = r"({.*?}|\[.*?\])"
        # groups: List[str] = re.findall(json_regex, out, re.DOTALL)

        # if groups != []:
        if first_idx != -1 and last_idx != -1:
            try:
                # print(groups)
                # obj = json.loads(groups[0])
                obj = json.loads(out[first_idx : last_idx + 1])
            except ValueError as e:
                print(e)
                attempts_remaining -= 1
                print(f"Retrying... attempts remaining: {attempts_remaining}")
                continue

        # if not same datatype, retry
        all_cols_valid = True
        column_values = {}

        for col in columns:
            if col.name not in obj or "value" not in obj[col.name]:
                print(f"Column {col.name} missing ({obj})")
                all_cols_valid = False
                continue

            value = obj[col.name]["value"]

            if value is not None and (
                (col.datatype == "string" and not isinstance(value, str))
                or (col.datatype == "boolean" and not isinstance(value, bool))
            ):
                print(f"Column {col.name} has wrong datatype ({value}: {col.datatype})")
                all_cols_valid = False
                continue

            if col.datatype == "integer" and isinstance(value, float):
                obj[col.name]["value"] = int(value)

            if col.datatype == "number" and isinstance(value, int):
                obj[col.name]["value"] = int(value)

            column_values[col.name] = obj[col.name]["value"]

            # TODO: check if answer is correct with another LLM
            # await check_value_valid(text=text, value=obj[col.name], column=col)

        if not all_cols_valid:
            attempts_remaining -= 1
            print(f"Retrying... attempts remaining: {attempts_remaining}")
            continue

        return column_values

    return None


async def process_node(text: str, column_embeddings: List[BaseEmbedding]):
    # key_values = await LLM.achat(
    #     messages=[
    #         ChatMessage(
    #             role="user",
    #             content=EXTRACT_KEY_VALUES_TEMPLATE.format(text=text),
    #         )
    #     ],
    # )
    key_values = await chat(EXTRACT_KEY_VALUES_TEMPLATE.format(text=text))

    columns = await get_target_column_names(
        key_values, CDS_COLUMNS, column_embeddings, 0.5
    )
    # print("possible columns:", columns)
    column_json = await get_column_json(key_values, columns)

    print(
        f"""
Original Text: {text}

Extracted Key Values: {key_values}

Extracted columns: {column_json}
    """
    )

    return column_json


async def process_column(column: Column, retriever: BaseRetriever):
    found_nodes = await retriever.aretrieve(
        column.name,
    )

    column_json = await get_column_json(
        text="\n\n".join([node.text for node in found_nodes]),
        columns=[column],
    )

    print(
        f"""
Column: {column.name}
Found Nodes: {found_nodes}
Column JSON: {column_json}
"""
    )

    return column_json


async def process_text_column_group(text: str, columns: List[Column]):
    column_json = await get_column_json(
        text=text,
        columns=columns,
    )

    #     print(
    #         f"""Text: {text}
    # Columns: {columns}
    # Column JSON: {column_json}
    # """
    #     )

    return column_json


async def create_dataframe(input_path: str, columns: List[Column]):
    nodes = await file_to_nodes(input_path)
    # column_embeddings = EMBED_MODEL.get_text_embedding_batch(
    #     texts=[column.name for column in CDS_COLUMNS],
    #     show_progress=True,
    # )
    # node_embeddings = EMBED_MODEL.get_text_embedding_batch(
    #     texts=[node.get_content(metadata_mode="embed") for node in nodes],
    #     show_progress=True,
    # )

    # cosine_sims = cosine_similarity(node_embeddings, column_embeddings)
    # # cosine_sims = euclidean_distances(node_embeddings, column_embeddings)

    # print("num nodes:", len(cosine_sims))
    # print("num cols:", len(cosine_sims[0]))

    # print("cosine sims:")
    # print(cosine_sims)

    # In [16]: np.argsort(a, axis=1)
    # Out[16]:
    # array([[0, 2, 1],
    #     [0, 2, 1],
    #     [1, 2, 0]])

    # In [17]: np.argsort(a, axis=0)
    # Out[17]:
    # array([[0, 2, 0], # smallest
    #     [1, 0, 1], # 2nd largest
    #     [2, 1, 2]]) # largest

    # In [18]: a
    # Out[18]:
    # array([[1, 5, 4],
    #     [3, 7, 6],
    #     [9, 2, 8]])

    # col_max_idxs = np.argmax(cosine_sims, axis=0)
    # print(f"col max idx ({len(col_max_idxs)}):", col_max_idxs)
    # col_sorted_idxs = np.argsort(cosine_sims, axis=0)
    # print(f"col sorted idxs ({len(col_sorted_idxs)}):", col_sorted_idxs)

    # col_20_max_node_idx = np.argmax(cosine_sims, axis=0)[20]

    # print("query:", CDS_COLUMNS[20].name)
    # print("max node idx:", col_20_max_node_idx)
    # print("max idx sim val:", cosine_sims[col_20_max_node_idx][20])
    # print(
    #     "col sorted node idxs:",
    #     [nth_node_sim_idxs[20] for nth_node_sim_idxs in col_sorted_idxs],
    # )
    # print(
    #     f"sorted node sims ({len(col_sorted_idxs)}):",
    #     [cosine_sims[col_sorted_idxs[i][20]][20] for i in range(len(col_sorted_idxs))],
    # )
    # print("most similar node:", nodes[col_20_max_node_idx])
    # print(
    #     "verify cosine sim:",
    #     cosine_similarity(
    #         [node_embeddings[col_20_max_node_idx]], [column_embeddings[20]]
    #     ),
    # )

    index = VectorStoreIndex(nodes=nodes, embed_model=EMBED_MODEL, show_progress=True)

    # retriever = index.as_retriever(similarity_top_k=2)
    # retriever_nodes = await retriever.aretrieve(CDS_COLUMNS[20].name)
    # print("nodes from retriever:", retriever_nodes)

    # get top 2 nodes for each column
    # group columns and nodes together
    # can have duplicate nodes but column sets must be disjoint
    # col_node_groups = [(i, []) for i, _ in enumerate(CDS_COLUMNS)]
    # top_k = 2

    # for i, nth_column_maxes in enumerate(col_sorted_idxs[-top_k:]):
    #     for j, col_nth_max_node_idx in enumerate(nth_column_maxes):
    #         # print(f"col {j} {-top_k+i}th max node:", col_nth_max_node_idx)
    #         col_node_groups[j][1].append(col_nth_max_node_idx)

    # print(
    #     f"top {top_k} nodes:",
    #     [
    #         (nodes[node_idx], cosine_sims[node_idx][20])
    #         for node_idx in col_node_groups[20][1]
    #     ],
    # )

    # go through node col node groups and combine those with same indexes
    # node_col_groups = {}

    # for col_idx, node_idxs in col_node_groups:
    #     # print(f"{CDS_COLUMNS[col_idx]}: {[nodes[i] for i in node_idxs]}")
    #     # print(f"{CDS_COLUMNS[col_idx]}: {node_idxs}")
    #     node_key = tuple(sorted(node_idxs))
    #     if node_key not in node_col_groups:
    #         node_col_groups[node_key] = [col_idx]
    #     else:
    #         node_col_groups[node_key].append(col_idx)

    # print(node_col_groups)
    coros = []

    # for node_group in node_col_groups:
    #     coro = process_text_column_group(
    #         text="\n\n".join([nodes[node_idx].text for node_idx in node_group]),
    #         columns=[CDS_COLUMNS[col_idx] for col_idx in node_col_groups[node_group]],
    #     )
    #     coros.append(coro)

    # retriever = index.as_retriever(similarity_top_k=4)
    retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": index.as_retriever(similarity_top_k=2)},
        node_dict={n.node_id: n for n in nodes},
        verbose=True,
    )

    for column in columns:
        coro = process_column(
            column,
            retriever,
        )
        coros.append(coro)

    # # for node in nodes[:20]:
    # #     coro = process_node(node.text, column_embeddings)
    # #     coros.append(coro)

    print("coroutines to process:", len(coros))

    # combine all fields
    column_values_generator = asyncio.as_completed(coros)
    all_values = {column.name: None for column in columns}

    for column_values_fut in column_values_generator:
        column_values = await column_values_fut

        if column_values is not None:
            all_values = {
                **all_values,
                **{
                    key: column_values[key]
                    for key in column_values
                    if column_values[key] is not None and key in all_values
                },
            }

    # save to parquet
    return pl.from_dict(all_values)


def lambda_handler(event, context):
    setup()

    print("recieved event:", event)

    try:
        bucket = event["detail"]["bucket"]["name"]
        filename: str = event["detail"]["object"]["key"]

        filepath = os.path.join("s3://", bucket, unquote_plus(filename))
        output_path = os.path.join(
            dataframes_bucket,
            os.path.dirname(filename),
            os.path.splitext(os.path.basename(filepath))[0] + ".parquet",
        )

        if not filename.endswith(".md"):
            print("Not an md file. Exiting")
            return

        print(f"processing file: {filepath} -> {output_path}")

        fs = s3fs.S3FileSystem()
        columns = []

        if "/cds" in filepath:
            columns = CDS_COLUMNS

        with tempfile.TemporaryDirectory() as tempdir:
            temp_in_file = os.path.join(tempdir, os.path.basename(filepath))
            temp_out_file = os.path.join(tempdir, os.path.basename(output_path))

            fs.get(filepath, tempdir)

            df = asyncio.run(
                create_dataframe(
                    input_path=temp_in_file,
                    columns=columns,
                )
            )

            df.write_parquet(temp_out_file)
            fs.put(temp_out_file, output_path)
    except Exception as e:
        print("Exception occured while converting tabular data:", e)


def main():
    setup()

    input_file = "../cds/md/purdue.md"
    output_file = "../cds/parquet/purdue.parquet"

    df = asyncio.run(
        create_dataframe(
            input_path=input_file,
            columns=CDS_COLUMNS,
        )
    )

    df.write_parquet(output_file)


if __name__ == "__main__":
    main()
