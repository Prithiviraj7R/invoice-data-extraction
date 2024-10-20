# Invoice PDF Data Extraction - ZOLVIT

## Overview
This invoice data extraction system is part of the Zolvit Problem Statement, designed to automate the extraction of key information from invoice PDFs. 

## Code Walkthrough

1) **data/processed:** stores the parse yaml output from PDF invoice
2) **requirements.txt:** contains all the dependencies
3) **src/pdf_extraction/pdf_to_text.py:** extracts text from PDF file
4) **src/pdf_extraction/parse_text_info.py:** parses the text and structures the invoice data
5) **src/utils/logger.py:** contains config for logging 
6) **src/utils/exception.py:** contains config for error handling
7) **src/main.py:** contains the code to extract data from all the invoices from test data

## Setup Instructions

``` bash
git clone https://github.com/Prithiviraj7R/invoice-data-extraction.git
cd invoice-data-extraction

pip install -r requirements.txt
python src/main.py
```

## Demo Instructions

``` bash
streamlit run demo.py
```

![Streamlit Demo Screen](<demo_screen.png>)

<video controls src="zolvit-demo.mp4" title="Title"></video>