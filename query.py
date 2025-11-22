# query.py - Simplified RAG brain (OpenAI + pure Python)
import streamlit as st
import os
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # numpy-based

# Load OpenAI key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Global: Simple in-memory chunks (loaded from ingest)
chunks = st.session_state.get("chunks", [])

# Simple embeddings function (OpenAI)
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

# Simple similarity search
def search_chunks(question, k=6):
    if not chunks:
        return []
    question_emb = get_embedding(question)
    chunk_embs = np.array([get_embedding(chunk["text"]) for chunk in chunks])
    similarities = cosine_similarity(question_emb.reshape(1, -1), chunk_embs)[0]
    top_indices = np.argsort(similarities)[::-1][:k]
    return [chunks[i] for i in top_indices]

# Generate answer with OpenAI
def ask(question):
    if not chunks:
        return "Please index the PDF first."
    docs = search_chunks(question)
    context = "\n\n".join([f"Page {doc['page']}: {doc['text']}" for doc in docs])
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Lightweight model
        messages=[
            {"role": "system", "content": "You are a North Carolina-licensed Professional Engineer with perfect knowledge of the 2024 North Carolina Residential Code (2021 IRC + NC amendments). Enforcement dates: Voluntary Jan 1, 2025; Mandatory Jul 1, 2025. Answer using ONLY the context below. Cite exact sections (e.g., R314.3.1). Be concise for plan review."},
            {"role": "user", "content": f"Question: {question}\nContext: {context}"}
        ],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content

# For app.py to use
