# app.py - Your live 2024 NC Residential Code AI
import streamlit as st
from query import ask
import os

st.set_page_config(page_title="2024 NC Residential Code AI", layout="centered")
st.title("2024 North Carolina Residential Code AI")
st.caption("Powered by your exact PDF + Claude 3.5 Sonnet ⋅ Built for NC Professional Engineers")

# ---- PDF Upload (only needed once) ----
if not os.path.exists("uploaded_pdf.pdf"):
    st.warning("Please upload your 2024 NC Residential Code PDF below (one-time step)")
    uploaded = st.file_uploader("Upload 2024_north_carolina_residential_code_updated.pdf", type="pdf")
    if uploaded:
        with open("uploaded_pdf.pdf", "wb") as f:
            f.write(uploaded.getbuffer())
        st.success("PDF uploaded! Now click the button below to index it (5–10 minutes).")
        if st.button("Index the PDF Now", type="primary"):
            st.switch_page("ingest.py")
else:
    st.success("✓ PDF is ready")

# ---- Indexing status ----
if not os.path.exists("nc_db"):
    st.info("Database not found. After uploading the PDF, click 'Index the PDF Now' above.")
else:
    st.success("✓ Database ready — you can ask questions!")

# ---- Chat interface ----
if os.path.exists("nc_db"):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything about the 2024 NC Residential Code…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching the exact code…"):
                answer = ask(prompt)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
