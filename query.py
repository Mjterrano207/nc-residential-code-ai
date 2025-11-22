# query.py - The RAG brain (Claude + your PDF)
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS  # ← New FAISS import
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os

# Load keys from secrets
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load the indexed database with FAISS
db = FAISS.load_local("./nc_db", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 6})

# Claude 3.5 Sonnet
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.0,
    max_tokens=4096
)

prompt = PromptTemplate.from_template("""
You are a North Carolina-licensed Professional Engineer with perfect knowledge of the 2024 North Carolina Residential Code (2021 IRC + NC amendments).
Enforcement dates:
• Voluntary use permitted: January 1, 2025
• Mandatory statewide: July 1, 2025
• 2018 code still applies until then
Answer using ONLY the retrieved sections below.
Always cite exact section numbers (e.g., R314.3.1, Table R507.5, or NC Amendment to R302.1).
Quote the code when helpful.
Question: {question}
Retrieved sections (page numbers included):
{context}
Answer in clear, concise language suitable for plan review:""")

def ask(question):
    docs = retriever.invoke(question)
    context = "\n\n".join([f"Page {d.metadata.get('page', '?')}: {d.page_content}" for d in docs])
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context}).content
