import os
import fitz
import requests as reqs
from pypdf import PdfReader


class PDFClass:

    def __init__(self,path=None,url=False):

        self.path = path
        self.url  = url
        self.title = self._title()

    def get_title(self):
        return self.title
    
    def _checklocalPDF(self):

        # check if file at this path is a pdf or not
        # check if file at this path is a pdf or not
        # check if file at this path is a pdf or not

        try:
            PdfReader(self.path)
        except Exception as e:
            print(str(e))
            return False
        
        return True

    def _checkonlinePDF(self):

        r = reqs.get(self.path,timeout=15)

        headers_to_check = ['content-type','content-disposition']
        for header in headers_to_check:
            if header in r.headers:
                if "pdf" in r.headers[header]:
                    return True
                
        return True

    def _maketemppdf(self):

        r = reqs.get(self.path,timeout=15)

        # write the pdf as a temp file
        with open("temp.pdf", "wb") as pdf_file:
            pdf_file.write(r.content)

        return "temp.pdf"

    def _extract_title(self):

        title = ""

        try:
            pdf_document = fitz.open(self.path)
            title = pdf_document.metadata.get("title", "Title not found")
            pdf_document.close()

            if self.url:
                # Delete the temp file if url was used
                os.remove(self.path)

        except Exception as e:
            title = "Unable to get title"
        
        return title

    def _title(self):

        ispdf = False

        if self.url:
            ispdf = self._checkonlinePDF()
            self.path  = self._maketemppdf()
        else:
            ispdf = self._checklocalPDF()

        if not ispdf:
            return "Not a PDF"
        
        return self._extract_title()

    def _section_headings(self):
        return ["test"]