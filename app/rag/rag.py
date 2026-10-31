from sentence_transformers import SentenceTransformer
import chromadb
import os

model = SentenceTransformer(
    "BAAI/bge-m3"
)

client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", "8006"))
)

collection = client.get_or_create_collection(
    "fablab"
)

def retrieve(query):

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    docs = results.get("documents", [[]])[0]
    if not docs:
        return "Nenhum documento encontrado na base de conhecimento."

    return "\n\n".join(docs)