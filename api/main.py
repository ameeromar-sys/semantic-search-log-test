from fastapi import FastAPI
from search import search # Ensure search.py is in the root or accessible

app = FastAPI()

@app.get("/search")
def semantic_search(query: str):
    results = search(query)
    return {"results": results}