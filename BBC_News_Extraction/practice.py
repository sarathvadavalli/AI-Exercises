import chromadb

client = chromadb.PersistentClient(path="/news/chroma_db")

# # Get a list of all collections
# collections = client.list_collections()

# # Print the names of the collections
# for collection in collections:
#     print(collection.name)


collection = client.get_collection("bbc_news")

print(collection.count())

data = collection.get(
    limit=5,
    include=["embeddings", "documents", "metadatas"]
)

embeddings = data['embeddings'][0]
print(len(embeddings))

for i in range(5):
    print(f"ID: {data['ids'][i]}")
    print(f"Document: {data['documents'][i]}")
    print(f"Metadata: {data['metadatas'][i]}")
    print(f"Embedding: {data['embeddings'][i]}")
    print("-" * 80)
