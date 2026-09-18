from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document


# 1. WEB CONTENT LOADER
class WebContentLoader:
    def __init__(self, urls: List[str]):
        self.urls = urls

    def load_content(self) -> List[Document]:
        try:
            loader = WebBaseLoader(self.urls)
            documents = loader.load()

            print(
                f"Successfully loaded content from "
                f"{len(documents)} documents"
            )

            return documents

        except Exception as e:
            print(f"Error loading content: {e}")
            return []

