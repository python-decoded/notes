import chromadb
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("Initializing db")

db_client = chromadb.PersistentClient("./chroma_db")
collection = db_client.get_or_create_collection(
    name="project_docs",
    metadata={"hnsw:space": "cosine"}
)


# RETRIEVE
request = "Що таке ембеддінг"
embedding = model.encode(request).tolist()
result = collection.query(
    embedding,
    n_results=5,
    # where={"file": "embedding.txt"},
    include=["documents", "metadatas", "distances"]
)

retrieved_items = list(zip(result["ids"][0],
                           result["distances"][0],
                           result["documents"][0]))

print(*retrieved_items, sep="\n")


# AUGMENT
retrieved_chunks = "\n".join(result["documents"][0])

prompt = f"""Використай цю інфу,
щоб відповісти на питання:

{retrieved_chunks}

Питання: '{request}'"""

# SEND REQUEST TO LLM
print(prompt)
