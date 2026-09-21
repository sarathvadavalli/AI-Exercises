import chromadb

# client = chromadb.PersistentClient(path="/content/chroma_db")

# collections = client.list_collections()

# if len(collections) == 0:
#     print("No collections found")
# else:
#     for collection in collections:
#         print(collection.name)

import os

print(os.path.exists("/content/chroma_db/"))
print(os.listdir("/content/chroma_db/"))