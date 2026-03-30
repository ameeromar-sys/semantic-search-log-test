# Semantic Log Search

A small pipeline for building a semantic search system over log files using Sentence-Transformers and FAISS.

## Project structure

- `preprocess_logs.py`: cleans raw log lines and writes normalized versions to `data/clean_logs.txt`.
- `build_index.py`: computes sentence embeddings for cleaned logs (`all-MiniLM-L6-v2`) and builds a FAISS index (`models/log_index.faiss`).
- `search.py`: loads model/index/data and exposes a `search(query, k=3)` function returning top-k similar logs.
- `api/main.py`: FastAPI endpoint `/search?query=<text>` that returns semantic search results.
- `streamlit_app.py`: simple Streamlit UI for text input and log result display.
- `data/`: input/output data files.
- `models/`: serialized FAISS index and embeddings.

## Requirements

- Python 3.8+
- `faiss` (CPU or GPU build)
- `sentence-transformers`
- `fastapi`, `uvicorn` (optional, for API)
- `streamlit` (optional, for UI)

Install with pip:

```bash
pip install sentence-transformers faiss-cpu fastapi uvicorn streamlit
```

> If your platform has a GPU and you're using GPU FAISS, change `faiss-cpu` to `faiss-gpu`.

## Getting started

1. Prepare raw logs:
   - Place your logs in `data/HDFS.log` (or adjust paths in the script).

2. Clean logs:

```bash
python preprocess_logs.py
```

3. Build embeddings and index:

```bash
python build_index.py
```

4. Run search in Python:

```python
from search import search
results = search("NameNode error")
print(results)
```

## API server (FastAPI)

Start server:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Call endpoint:

```bash
curl "http://127.0.0.1:8000/search?query=timeout"
```

## Streamlit UI

Start app:

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` and enter your query.

## Customization

- Swap out the embedding model in `build_index.py` and `search.py` for another `SentenceTransformer` model to adjust accuracy and speed.
- Adjust preprocessing logic in `preprocess_logs.py` to fit your log format.
- Increase `k` in `search(query, k=...)` for more results.

## Notes

- `search.py` uses deduplicated logs (`set(clean_logs)`) so identical lines are stored once.
- You can point `preprocess_logs.py` at another input file by editing `input_file`.
- Re-run all steps whenever source logs change.
