from langchain_core.tools import tool
import io
import PyPDF2
import requests
url="http://arxiv.org/pdf/2508.14042v1"



@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL
    Args:
        url (str): The URL of the PDF file to read.
    
    Returns:
        str: The extracted text from the PDF file.
    """
    try:
        #step1: access PDF by url
        response = requests.get(url)

        #step2: convert to Bytes
        pdf_file = io.BytesIO(response.content)

        #step3: retirieve text from pdf
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # print(len(pdf_reader.pages))
        num_pages = len(pdf_reader.pages)
        texts = ""
        for i, page in enumerate(pdf_reader.pages,1):
            # print(f"Extracting text from page {i} of {num_pages}")
            texts += page.extract_text() + "\n"
        # print(f"Successfully extracted {len(texts)} characters of text from {num_pages} pages.")
        return texts.strip()
    except Exception as e:
        print(f"Error reading PDF from {url}: {e}")
        raise

print(read_pdf(url))  # Example usage, replace with your URL