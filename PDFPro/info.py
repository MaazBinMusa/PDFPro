import os
import fitz
import requests as reqs
from pypdf import PdfReader

PDFPATH = "None"
URL = False

def checklocalPDF(path):

    # check if file at this path is a pdf or not
    # check if file at this path is a pdf or not
    # check if file at this path is a pdf or not

    try:
        PdfReader(path)
    except Exception as e:
        print(str(e))
        return False
    
    return True

def checkonlinePDF(path):

    r = reqs.get(path,timeout=15)

    headers_to_check = ['content-type','content-disposition']
    for header in headers_to_check:
        if header in r.headers:
            if "pdf" in r.headers[header]:
                return True
            
    return True

def maketemppdf(path):

    r = reqs.get(path,timeout=15)

    # write the pdf as a temp file
    with open("temp.pdf", "wb") as pdf_file:
        pdf_file.write(r.content)

    return "temp.pdf"

def extract_title(path,url):

    title = ""

    try:
        pdf_document = fitz.open(path)
        title = pdf_document.metadata.get("title", "Title not found")
        pdf_document.close()

        if url:
            # Delete the temp file if url was used
            os.remove(path)

    except Exception as e:
        title = "Unable to get title"
    
    return title

def title(path,url=False):

    ispdf = False

    if url:
        ispdf = checkonlinePDF(path)
        path  = maketemppdf(path)
    else:
        ispdf = checklocalPDF(path)

    if not ispdf:
        return "Not a PDF"
    
    return extract_title(path,url)

def section_headings(path,url=False):
    return ["test"]