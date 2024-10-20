# Text Extraction from PDF files (Normal File, Not Scanned)

import os
import sys
import PyPDF2 # type: ignore
from src.utils.exception import CustomException
from src.utils.logger import logging

def pdf_to_text(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    :param pdf_path: Path to the PDF file.
    :return: Text extracted from the PDF file.
    """

    text = ""

    try:
        with open(pdf_path, 'rb') as file:
            logging.info(f"Extracting text from PDF file: {pdf_path}")
            pdf = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                text += page.extract_text()
            
            logging.info("Text extracted successfully from PDF file.")

    except Exception as e:
        raise CustomException(e, sys)

    return text


if __name__ == "__main__":
    pdf_path = r"D:\Placements\Zolvit\invoice-data-extraction\data\raw\INV-117_Naman.pdf"
    text = pdf_to_text(pdf_path)
    print(text)