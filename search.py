import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("models/log_index.faiss")

with open("data/clean_logs.txt") as f:
    logs = [line.strip() for line in f]

clean_logs = list(set(logs))


def search(query, k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding), k
    )

    results = [clean_logs[i] for i in indices[0]]
    return results