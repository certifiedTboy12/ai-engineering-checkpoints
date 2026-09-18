# Install the required packages first:
# pip install sentence-transformers faiss-cpu numpy

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# 1. Prepare the Document Corpus
corpus = [
    "Artificial Intelligence is transforming industries.",
    "FAISS enables efficient vector similarity search.",
    "Machine learning models require high-quality data.",
    "Python is widely used for data science tasks.",
    "AI helps businesses automate repetitive processes.",
    "Deep learning is commonly used for image recognition.",
    "Natural language processing allows computers to understand human language.",
    "Companies use AI to improve customer service and personalization.",
    "Data science combines statistics, programming, and machine learning.",
    "Cloud computing provides scalable infrastructure for AI applications."
]

print(f"Number of documents: {len(corpus)}")



# 2. Generate Embeddings
# Load a pre-trained sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert each document into a vector
embeddings = model.encode(
    corpus,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)



# 3. Build the FAISS Index
# Dimension of the embeddings
d = embeddings.shape[1]

# Create a FAISS index using Euclidean/L2 distance
index = faiss.IndexFlatL2(d)

# Add document embeddings to the index
index.add(np.array(embeddings).astype("float32"))

print("Number of vectors in FAISS index:", index.ntotal)



# 4. Test Retrieval
query = "How can I use AI in industry?"

# Convert the query into an embedding
query_vector = model.encode(
    [query],
    convert_to_numpy=True
).astype("float32")

# Search for the top 2 most similar documents
D, I = index.search(query_vector, k=2)

print("\nQuery:", query)
print("\nTop Results:")

for rank, idx in enumerate(I[0], start=1):
    print(f"{rank}. {corpus[idx]}")
    print(f"   Distance: {D[0][rank - 1]:.4f}")