import streamlit as st # type: ignore
import os
import sys

from src.utils.exception import CustomException
from src.utils.logger import logging
from src.pdf_extraction.pdf_to_text import pdf_to_text
from src.pdf_extraction.parse_text_info import parse_text

def main():
    # streamlit app for Demo
    st.title("PDF Invoice Data Extraction")

    # upload a PDF file
    uploaded_file = st.file_uploader("Choose an invoice in PDF format", type="pdf")

    if uploaded_file is not None:
        with open("tmp.pdf", "wb") as file:
            file.write(uploaded_file.getbuffer())

        try:

            # extract text from PDF
            text = pdf_to_text("tmp.pdf")
            yaml_output = parse_text(text)

            st.subheader("Extracted Invoice Data:")
            st.text_area("Invoice", value=yaml_output, height=300)

            # save the extracted data to a YAML file

            file_name = os.path.splitext(uploaded_file.name)[0] + ".yaml"
            yaml_file_path = os.path.join("demo", file_name)
            os.makedirs("demo", exist_ok=True)

            with open(yaml_file_path, "w") as yaml_file:
                yaml_file.write(yaml_output)

            st.success(f"YAML file saved: {yaml_file_path}")

        except Exception as e:
            raise CustomException(e, sys)
        
        finally:
            # remove the temporary PDF file
            
            if os.path.exists("tmp.pdf"):
                os.remove("tmp.pdf")

if __name__ == "__main__":
    main()