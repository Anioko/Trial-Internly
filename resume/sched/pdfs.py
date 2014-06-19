from xhtml2pdf import pisa
from StringIO import StringIO

def create_pdf(pdf_data):
    # Here could go some special options about creating the pdf file
    pdf = StringIO()
    pisa.CreatePDF(pdf_data,dest=pdf,encoding='utf-8')
    print pdf_data
    return pdf