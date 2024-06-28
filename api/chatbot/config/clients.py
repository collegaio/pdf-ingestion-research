from llama_index.llms.openai import OpenAI
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.llms.cohere import Cohere

from chatbot.chat.models import CDSDataset
from chatbot.adapters.pinecone import PineconeAdapter
from chatbot.adapters.datasets import DatasetsFile, load_datasets_file
from chatbot.adapters.cohere import CohereChatAdapter
from chatbot.config.env import COHERE_API_KEY, OPENAI_API_KEY, PINECONE_API_KEY


cohere_llm = Cohere(model="command-r-plus", api_key=COHERE_API_KEY)
gpt_llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4-turbo")
gpt_embedding_model = OpenAIEmbedding(
    api_key=OPENAI_API_KEY, model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
)
pinecone_adapter = PineconeAdapter(api_key=PINECONE_API_KEY)


# TODO: move datasets file over
# datasets = load_datasets_file("../datasets.json")
datasets = DatasetsFile(cds_files=[])

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
