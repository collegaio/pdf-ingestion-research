from llama_index.core.indices import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.base.embeddings.base import BaseEmbedding
from pinecone import Pinecone


class PineconeAdapter:
    def __init__(self, api_key: str):
        self.pc = Pinecone(api_key=api_key)

    def get_index(self, index_name: str, embed_model: BaseEmbedding):
        return VectorStoreIndex.from_vector_store(
            vector_store=PineconeVectorStore(self.pc.Index(index_name)),
            embed_model=embed_model,
        )
