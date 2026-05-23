import chromadb
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("Initializing db")

db_client = chromadb.PersistentClient("./chroma_db")
collection = db_client.get_or_create_collection(
    name="project_docs",
    metadata={"hnsw:space": "cosine"}
)


import os
import textwrap

print("Starting chunking")
for current_folder, folders, files in os.walk("data"):
    for file_name in files:
        with open(os.path.join(current_folder, file_name), "r", encoding="utf-8") as f:
            content = f.read()
            for _idx, chunk in enumerate(textwrap.wrap(content, width=500), start=1):

                print(current_folder, file_name, _idx, chunk)
                embedding = model.encode(chunk).tolist()

                collection.add(
                    ids=[f"{file_name}_{_idx}"],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas={"file": file_name, "folder": current_folder}
                )
