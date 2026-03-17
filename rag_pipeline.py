import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

def build_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(chunks, embeddings)


def generate_ddr(vectorstore):

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    prompt = ChatPromptTemplate.from_template("""
You are an expert building inspection analyst.

Generate a Detailed Diagnostic Report (DDR).

STRICT FORMAT:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

RULES:
- Use ONLY provided context
- Do NOT invent anything
- If missing → write "Not Available"
- If conflict → mention clearly
- Use simple client-friendly language

CONTEXT:
{context}

REQUEST:
Generate the DDR report.
""")

    doc_chain = create_stuff_documents_chain(llm, prompt)

    chain = create_retrieval_chain(retriever, doc_chain)

    result = chain.invoke({"input": "Generate DDR"})

    return result["answer"]