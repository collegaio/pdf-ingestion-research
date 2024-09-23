from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone
import boto3

from chatbot.config import env
from chatbot.adapters.datasets import (
    DatasetsConfig,
    load_datasets,
)

from chatbot.config.env import PINECONE_API_KEY

bedrock_client = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=env.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
    region_name=env.AWS_REGION,
)
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

cohere_langchain_llm = ChatBedrockConverse(
    # credentials_profile_name="collega-prod",
    client=bedrock_client,
    model="cohere.command-r-v1:0",
    # streaming=True,
)

cohere_langchain_embed_model = BedrockEmbeddings(
    client=bedrock_client, model_id="cohere.embed-english-v3"
)

collega_datasets_index = pinecone_client.Index("collega-datasets")
collega_datasets_vectorstore = PineconeVectorStore(
    index=collega_datasets_index,
    embedding=cohere_langchain_embed_model,
    text_key="_node_content",
)

dataset_config = DatasetsConfig(
    **{
        "datasets": {
            "cds_files": {
                "properties": {
                    "description": "Answers questions about admissions data from 2023 onward such as GPA, standardized test scores, demographic data, and financial aid award sizes",
                    "datapoint_prefix": "Admissions data for ",
                }
            },
            "training_info": {
                "properties": {
                    "description": "Guides for applying to college",
                    "datapoint_prefix": "",
                }
            },
        }
    }
)

datasets = load_datasets(dataset_config)


# cds_query_tool = create_cds_query_router(
#     datasets=datasets.cds_files,
#     llm=gpt_llm,
#     index=pinecone_adapter.get_index("cds-index-test", embed_model=gpt_embedding_model),
# )

# tool_index = ObjectIndex.from_objects(
#     # [college_lookup_tool, cds_query_tool],
#     [cds_query_tool],
#     index_cls=VectorStoreIndex,
# )

# tool_retriever = tool_index.as_retriever(llm=gpt_llm, verbose=True)

# tools = tool_retriever.retrieve("space exploration")
# print(tools)

# chat_handler = CohereChatAdapter(
#     api_key=COHERE_API_KEY,
#     # tools=[college_lookup_tool, cds_query_tool],
#     tool_retriever=tool_index.as_retriever(llm=gpt_llm, verbose=True),
# )
