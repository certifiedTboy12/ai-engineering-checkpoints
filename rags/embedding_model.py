from langchain_huggingface import (
    HuggingFaceEmbeddings
)



# 3. HUGGING FACE EMBEDDINGS
class EmbeddingModel:

    def __init__(
        self,
        model_name: str = "BAAI/bge-base-en-v1.5"
    ):

        print(f"Loading embedding model: {model_name}")

        # Runs locally using sentence-transformers.
        # No Hugging Face inference API call is required.
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    def get_embeddings(self):
        return self.embeddings

