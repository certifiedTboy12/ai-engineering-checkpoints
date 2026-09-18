# 6. RESPONSE GENERATOR

# class ResponseGenerator:

#     def __init__(
#         self,
#         model_id: str = "HuggingFaceH4/zephyr-7b-beta"
#     ):
#         hf_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")

#         if not hf_token:
#             raise ValueError(
#                 "HUGGINGFACEHUB_API_TOKEN environment variable "
#                 "is not set."
#             )

#         self.model = HuggingFaceEndpoint(
#             repo_id=model_id,
#             huggingfacehub_api_token=hf_token,
#             temperature=0.2,
#             max_new_tokens=512
#         )

#     def create_qa_chain(self, retriever):

#         prompt = ChatPromptTemplate.from_template(
#             """
# You are a helpful AI assistant.

# Answer the question using ONLY the information contained
# in the provided context.

# If the answer cannot be found in the context, say:
# "I don't know based on the provided context."

# Do not invent information.

# Context:
# {context}

# Question:
# {input}

# Answer:
# """
#         )

#         # Chain that combines retrieved documents with the prompt
#         document_chain = create_stuff_documents_chain(
#             self.model,
#             prompt
#         )

#         # Retrieval + document chain
#         retrieval_chain = create_retrieval_chain(
#             retriever,
#             document_chain
#         )

#         return retrieval_chain


from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)



class ResponseGenerator:

    def __init__(
        self,
        model_name: str = "llama3.1:8b"
    ):

        self.model = ChatOllama(
            model=model_name,
            temperature=0
        )

    def create_qa_chain(self, retriever):

        prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.

Answer the question using ONLY the information provided
in the context below.

If the answer cannot be found in the context, say:
"I don't know based on the provided context."

Do not make up information.

Context:
{context}

Question:
{input}

Answer:
"""
        )

        document_chain = create_stuff_documents_chain(
            self.model,
            prompt
        )

        retrieval_chain = create_retrieval_chain(
            retriever,
            document_chain
        )

        return retrieval_chain