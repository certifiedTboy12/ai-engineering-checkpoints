
# 7. COMPLETE RAG PIPELINE

# class RAGPipeline:

#     def __init__(self, urls: List[str]):

#         self.loader = WebContentLoader(urls)

#         self.chunker = DocumentChunker()

#         self.embeddings = EmbeddingModel()

#         self.vectorstore = None
#         self.retriever = None
#         self.qa_chain = None

#     def build(self):

#         # Step 1: Load web pages
#         documents = self.loader.load_content()

#         if not documents:
#             raise ValueError(
#                 "No documents were loaded from the URLs."
#             )

#         # Step 2: Split documents into chunks
#         chunks = self.chunker.create_chunks(documents)

#         if not chunks:
#             raise ValueError(
#                 "No document chunks were created."
#             )

#         # Step 3: Create embeddings
#         embedding_model = self.embeddings.get_embeddings()

#         # Step 4: Create vector database
#         vector_store = VectorStore(embedding_model)

#         self.vectorstore = vector_store.create_store(chunks)

#         # Step 5: Create retriever
#         retriever_component = Retriever(
#             self.vectorstore
#         )

#         self.retriever = retriever_component.get_retriever()

#         # Step 6: Create LLM and RAG chain
#         generator = ResponseGenerator()

#         self.qa_chain = generator.create_qa_chain(
#             self.retriever
#         )

#         print("RAG pipeline built successfully.")

#     def query(self, question: str) -> str:

#         if self.qa_chain is None:
#             raise RuntimeError(
#                 "The RAG pipeline has not been built. "
#                 "Call build() first."
#             )

#         response = self.qa_chain.invoke(
#             {
#                 "input": question
#             }
#         )

#         return response["answer"]

from web_searcher import WebSearcher
from document_chunker import DocumentChunker
from embedding_model import EmbeddingModel
from web_content_loader import WebContentLoader
from vector_store import VectorStore
from retriever import Retriever
from response_generator import ResponseGenerator


class RAGPipeline:

    def __init__(self):

        self.searcher = WebSearcher()

        self.loader = None
        self.chunker = DocumentChunker()
        self.embeddings = EmbeddingModel()

        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None

    def build(self, query: str):

        # 1. Search web
        urls = self.searcher.search(query)

        if not urls:
            raise ValueError(
                "No relevant URLs were found."
            )

        # 2. Load web pages
        self.loader = WebContentLoader(urls)

        documents = self.loader.load_content()

        if not documents:
            raise ValueError(
                "No documents could be loaded."
            )

        # 3. Split documents
        chunks = self.chunker.create_chunks(
            documents
        )

        # 4. Create embeddings
        embedding_model = (
            self.embeddings.get_embeddings()
        )

        # 5. Create Chroma
        vector_store = VectorStore(
            embedding_model
        )

        self.vectorstore = (
            vector_store.create_store(chunks)
        )

        # 6. Create retriever
        retriever_component = Retriever(
            self.vectorstore
        )

        self.retriever = (
            retriever_component.get_retriever()
        )

        # 7. Create RAG chain
        generator = ResponseGenerator(
            model_name="llama3.1:8b"
        )

        self.qa_chain = (
            generator.create_qa_chain(
                self.retriever
            )
        )

        print("\nRAG pipeline successfully built!")

    def query(self, question: str) -> str:

        response = self.qa_chain.invoke({
            "input": question
        })

        return response["answer"]
