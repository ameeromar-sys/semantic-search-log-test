from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


with open("data/clean_logs.txt") as f:
    logs = [line.strip() for line in f]

clean_logs = list(set(logs))

embeddings = model.encode(clean_logs)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "models/log_index.faiss")
np.save("models/log_embeddings.npy", embeddings)