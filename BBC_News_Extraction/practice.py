import chromadb
import numpy as np


path = 'D:\AI Projects\RAG Practice\BBC_News_Extraction\chroma_db'
client = chromadb.PersistentClient(path=path)

# # Get a list of all collections
# collections = client.list_collections()
# for collection in collections:
#     print(collection.name)

# collection = client.create_collection(
#     name="bbc_news",
#     metadata={"hnsw:space": "ip"},
# )

collection = client.get_collection("bbc_news")

print(collection.count())

# Check if the collection uses inner product method for similarity search
metric = "l2 (default)"
if collection.metadata and "hnsw:space" in collection.metadata:
    metric = collection.metadata["hnsw:space"]

print(f"The active distance metric for this collection is: '{metric}'")

# Fetch top 5 documents from the collection
data = collection.get(
    limit=5,
    include=["embeddings", "documents", "metadatas"]
)

embeddings = data['embeddings'][0]
print(len(embeddings))

# Check if the embeddings are normalized
print("Embeddings magnitudes:")
for ind, embedding in enumerate(data["embeddings"]):
    magnitude = np.linalg.norm(embedding)
    print(f"Document-{ind+1}: {magnitude}")