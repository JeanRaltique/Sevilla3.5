from load_channels import get_file_name
from matplotlib.backends.backend_pdf import PdfPages

def pdf_report_creator(file_path):

    # Open files to save imgs and txt
    PDFName = get_file_name(file_path) + 'testpeak.pdf'
    pp = PdfPages(file_path + PDFName)
    TXTName = PDFName[:-4] + '.txt'
    REPORTfile = open(file_path + TXTName, "w")  # REPORT FILE

    return pp, REPORTfile