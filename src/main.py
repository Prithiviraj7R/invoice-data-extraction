from src.utils.exception import CustomException
from src.utils.logger import logging
import sys
import os

from src.pdf_extraction.pdf_to_text import pdf_to_text
from src.pdf_extraction.parse_text_info import parse_text

def main(pdf_file_path):

    # extract text from pdf
    text = ""
    try:
        text = pdf_to_text(pdf_file_path)
        # print(text)

    except CustomException as e:
        raise CustomException(e, sys)

    # parse text to get required information
    yaml_output = ""
    try:
        yaml_output = parse_text(text)

    except CustomException as e:
        raise CustomException(e, sys)
    
    # store the information in a yaml file
    file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
    os.makedirs("data/processed", exist_ok=True)
    yaml_file_path = os.path.join("data/processed", file_name + ".yaml")

    with open(yaml_file_path, "w") as yaml_file:
        yaml_file.write(yaml_output)

    logging.info("Information extracted from the PDF file and stored in yaml file.")


if __name__ == "__main__":
    folder_path = "data/raw"
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, file)
            main(pdf_file_path)

