# Web Search RAG with LangChain, Chroma, Hugging Face Embeddings, and Ollama

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** application that can automatically search the web for relevant information and use that information to answer user questions.

Instead of manually providing URLs, the application accepts a question such as:

```text
What is a recurrent neural network?
```

It then:

1. Searches the web for relevant pages.
2. Extracts the URLs from the search results.
3. Loads the web pages.
4. Splits the pages into smaller document chunks.
5. Converts the chunks into vector embeddings.
6. Stores the embeddings in Chroma.
7. Retrieves the most relevant chunks for the user's question.
8. Sends the retrieved context to a local Ollama LLM.
9. Generates an answer based on the retrieved information.

The overall architecture is:

```text
                         User Question
                               |
                               v
                       Web Search (Tavily)
                               |
                               v
                         Relevant URLs
                               |
                               v
                        WebBaseLoader
                               |
                               v
                           Documents
                               |
                               v
                 RecursiveCharacterTextSplitter
                               |
                               v
                            Chunks
                               |
                               v
                 Hugging Face Embeddings
                  BAAI/bge-base-en-v1.5
                               |
                               v
                            Chroma
                         Vector Store
                               |
                               v
                          Retriever
                               |
                               v
                    Relevant Document Chunks
                               |
                               v
                       RAG Prompt + Context
                               |
                               v
                       Ollama Llama 3.1
                            8B Model
                               |
                               v
                            Answer
```

---

# 1. Technologies Used

The application uses the following technologies:

| Technology                     | Purpose                              |
| ------------------------------ | ------------------------------------ |
| Python                         | Application programming language     |
| LangChain                      | RAG application framework            |
| Tavily                         | Automatic web search                 |
| WebBaseLoader                  | Loads web page content               |
| RecursiveCharacterTextSplitter | Splits documents into chunks         |
| Hugging Face                   | Provides the embedding model         |
| BGE                            | Converts text into vector embeddings |
| Chroma                         | Vector database                      |
| Ollama                         | Runs the local language model        |
| Llama 3.1 8B                   | Generates the final answer           |
| Sentence Transformers          | Runs embeddings locally              |

---

# 2. Why RAG?

A language model has knowledge that may not contain the specific information required by a question.

RAG solves this problem by retrieving external information before generating the answer.

For example, if the user asks:

```text
What are the current applications of recurrent neural networks?
```

the application searches the web and retrieves relevant information.

The retrieved information becomes the context given to the language model.

Instead of:

```text
Question
   |
   v
LLM
   |
   v
Answer
```

the application uses:

```text
Question
   |
   v
Search
   |
   v
Documents
   |
   v
Relevant Context
   |
   v
LLM
   |
   v
Answer
```

This allows the model to answer questions using retrieved external information.

---

# 3. Project Structure

A simple project structure is:

```text
ollama-llm/
│
├── rag.py
├── README.md
├── .env
├── .gitignore
│
└── venv/
```

The main application is:

```text
rag.py
```

The `.env` file stores the Tavily API key.

The `venv` directory contains the Python virtual environment.

---

# 4. Requirements

Before running the project, install:

- Python
- Ollama
- Llama 3.1 8B
- Tavily API key
- Required Python packages

## Recommended Python Version

For this project, Python 3.11 or Python 3.12 is recommended.

Although newer Python versions may work, some machine-learning packages can take time to catch up with the latest Python releases.

Check your Python version:

```bash
python --version
```

Example:

```text
Python 3.12.10
```

---

# 5. Create a Virtual Environment

Navigate to your project directory:

```bash
cd C:\Users\dell\Desktop\ollama-llm
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

You should see something similar to:

```text
(venv) C:\Users\dell\Desktop\ollama-llm>
```

---

# 6. Install Required Packages

Install the required packages:

```bash
pip install -U langchain
pip install -U langchain-classic
pip install -U langchain-community
pip install -U langchain-core
pip install -U langchain-text-splitters
pip install -U langchain-huggingface
pip install -U langchain-chroma
pip install -U langchain-ollama
pip install -U sentence-t
```
