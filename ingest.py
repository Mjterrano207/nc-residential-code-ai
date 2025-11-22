# ingest.py - Run this once to index your 2024 NC Residential Code PDF
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # ← OpenAI embeddings
from langchain_community.vectorstores import FAISS  # ← FAISS vector store

st.title("Indexing 2024 NC Residential Code")
st.write("This only needs to run once. It will take 3–5 minutes.")

pdf_path = "uploaded_pdf.pdf"

if not st.session_state.get("indexed", False):
    if st.button("Start Indexing the PDF Now", type="primary"):
        with st.spinner("Loading and processing 830+ pages..."):
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            st.success(f"Loaded {len(documents)} pages")

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)
            st.info(f"Split into {len(chunks)} chunks")

            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            vectorstore = FAISS.from_documents(chunks, embeddings)
            vectorstore.save_local("./nc_db")

        st.session_state.indexed = True
        st.success("Indexing complete! Your AI is ready.")
        st.balloons()
else:
    st.success("Already indexed! You can close this page.")
