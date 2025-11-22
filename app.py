# app.py - Handles 3 split parts automatically
import streamlit as st
import os
from query import ask
st.set_page_config(page_title="2024 NC Residential Code AI", layout="centered")
st.title("2024 North Carolina Residential Code AI")
st.caption("Powered by your exact PDF + Claude 3.5 Sonnet")

# ---- Auto-combine 3 split PDFs (runs only once) ----
FINAL_PDF = "uploaded_pdf.pdf"

if not os.path.exists(FINAL_PDF):
    st.info("Combining your 3 PDF parts (44 MB total)… this takes ~30 seconds")
    from PyPDF2 import PdfMerger

    merger = PdfMerger()
    merger.append("uploaded_pdf_part1.pdf")
    merger.append("uploaded_pdf_part2.pdf")
    merger.append("uploaded_pdf_part3.pdf")
    merger.write(FINAL_PDF)
    merger.close()
    st.success("PDF successfully combined and ready!")

# ---- Rest is unchanged ----
if not os.path.exists("nc_db"):
    st.info("PDF ready — now index it once (5–10 minutes)")
    if st.button("Index the PDF Now", type="primary"):
        st.switch_page("ingest.py")
else:
    st.success("Database ready — ask questions below!")

if os.path.exists("nc_db"):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything about the 2024 NC Residential Code…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching the code…"):
                answer = ask(prompt)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.markdown("Voluntary Jan 1, 2025 • Mandatory Jul 1, 2025")
