# ingest.py - Simple PDF chunking (no LangChain)
import streamlit as st
from pypdf2 import PdfReader
import os

st.title("Indexing 2024 NC Residential Code")
st.write("This only needs to run once. It will take 1–2 minutes.")

pdf_path = "uploaded_pdf.pdf"

if not st.session_state.get("indexed", False):
    if st.button("Start Indexing the PDF Now", type="primary"):
        with st.spinner("Loading and processing PDF..."):
            if not os.path.exists(pdf_path):
                st.error("PDF not found. Ensure uploaded_pdf.pdf is in repo.")
                st.stop()

            reader = PdfReader(pdf_path)
            chunks = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                # Simple chunking: Split by paragraphs
                paragraphs = text.split('\n\n')
                for para in paragraphs:
                    if len(para.strip()) > 50:  # Skip short text
                        chunks.append({"text": para.strip(), "page": i+1})
            
            st.session_state.chunks = chunks
            st.session_state.indexed = True
            st.success(f"Indexed {len(chunks)} chunks from {len(reader.pages)} pages! Your AI is ready.")
            st.balloons()
else:
    st.success("Already indexed!")
