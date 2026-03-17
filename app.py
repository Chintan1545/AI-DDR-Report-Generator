import streamlit as st
import os

from pdf_utils import load_and_split_pdfs
from image_utils import extract_images
from rag_pipeline import build_vectorstore, generate_ddr

st.set_page_config(page_title="DDR Generator", layout="wide")

st.title("🏗 AI DDR Report Generator")

inspection = st.file_uploader("Upload Inspection Report", type="pdf")
thermal = st.file_uploader("Upload Thermal Report", type="pdf")

if st.button("Generate DDR"):

    if inspection and thermal:

        os.makedirs("data", exist_ok=True)

        with open("data/inspection.pdf", "wb") as f:
            f.write(inspection.read())

        with open("data/thermal.pdf", "wb") as f:
            f.write(thermal.read())

        st.info("Processing PDFs...")

        chunks = load_and_split_pdfs([
            "data/inspection.pdf",
            "data/thermal.pdf"
        ])

        vectorstore = build_vectorstore(chunks)

        st.info("Extracting images...")

        imgs1 = extract_images("data/inspection.pdf")
        imgs2 = extract_images("data/thermal.pdf")

        st.info("Generating DDR Report...")

        report = generate_ddr(vectorstore)

        st.subheader("📄 DDR Report")
        st.write(report)

        st.subheader("🖼 Extracted Images")

        for img in imgs1 + imgs2:
            st.image(img, width=400)

    else:
        st.warning("Please upload both PDFs.")