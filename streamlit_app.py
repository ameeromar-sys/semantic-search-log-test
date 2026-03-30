import streamlit as st
from search import search

st.title("Semantic Log Search")

query = st.text_input("Search logs")

if query:
    results = search(query)

    for r in results:
        st.write(r)