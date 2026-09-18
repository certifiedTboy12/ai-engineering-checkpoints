from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from dotenv import load_dotenv


load_dotenv()
# 2. DOCUMENT CHUNKER
class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_chunks(
        self,
        documents: List[Document]
    ) -> List[Document]:

        chunks = self.splitter.split_documents(documents)

        print(
            f"Created {len(chunks)} chunks "
            f"from {len(documents)} documents"
        )

        return chunks
