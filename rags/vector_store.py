from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List



# 4. VECTOR STORE
class VectorStore:

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vectorstore = None

    def create_store(
        self,
        documents: List[Document]
    ) -> Chroma:

        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="web_rag_collection"
        )

        print("Chroma vector store created successfully.")

        return self.vectorstore




