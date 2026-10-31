from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os
import uuid

# Adjust these values based on the embedding model's max token limit.
# BAAI/bge-m3 has a large context window, but chunking is still required 
# to ensure granular and precise vector search results.
CHUNK_SIZE = 1000
OVERLAP = 200

model = SentenceTransformer("BAAI/bge-m3")

client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", "8006"))
)

collection = client.get_or_create_collection(name="fablab")

DATA_DIR = "data"
documents = []

def chunk_text(text, chunk_size, overlap):
    """
    Splits a large text into smaller overlapping chunks (sliding window).
    This prevents truncation by the embedding model and improves retrieval accuracy.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(root, file)
            
            try:
                reader = PdfReader(path)
                text = ""
                
                for page in reader.pages:
                    extracted = page.extract_text()
                    # extract_text() might return None on image-based pages
                    if extracted:
                        text += extracted + " "
                
                chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)
                
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        documents.append({
                            # UUID prevents overwrite collisions on multiple runs
                            "id": f"{file}_chunk_{i}_{uuid.uuid4().hex[:6]}",
                            "source": file,
                            "chunk_index": i,
                            "content": chunk
                        })
            except Exception as e:
                # Silently skip unreadable/corrupted PDFs to keep the pipeline running
                print(f"Skipping {file} due to error: {e}")

if documents:
    texts_to_encode = [doc["content"] for doc in documents]
    
    # Batch encoding to maximize processing speed
    embeddings = model.encode(texts_to_encode, show_progress_bar=True).tolist()

    ids = [doc["id"] for doc in documents]
    metadatas = [{"source": doc["source"], "chunk_index": doc["chunk_index"]} for doc in documents]

    # Batch insert into vector DB
    collection.add(
        ids=ids,
        documents=texts_to_encode,
        metadatas=metadatas,
        embeddings=embeddings
    )
    print("Documents indexed.")
else:
    print("No documents were found or processed.")