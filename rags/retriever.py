from langchain_chroma import Chroma

# 5. RETRIEVER
class Retriever:

    def __init__(
        self,
        vectorstore: Chroma,
        k: int = 4
    ):

        self.retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": 10
            }
        )

    def get_retriever(self):
        return self.retriever
