from docx2txt import process
from os import listdir, mkdir
from shutil import rmtree
from string import printable
from os.path import isfile, join, splitext, exists
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from pdfminer.pdfparser import PDFSyntaxError


class Docxer:
    def __init__(self):
        self.name = ""

    @staticmethod
    def get_folder(path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def run_files(self, dirs, ready_files, output=""):
        if exists(output):
            rmtree(output)
        mkdir(output)
        for file in ready_files:
            extension = splitext(dirs + file)[1]
            if "docx" in extension:
                to_write = str(self.process_doxc(dirs + file).encode('ascii', 'ignore'))
            elif "pdf" in extension:
                try:
                    to_write = str(self.process_pdf(dirs + file))
                except (PDFSyntaxError, Exception):
                    to_write = ""
            else:
                tofile = open(dirs + file)
                to_write = str(tofile.read())
                tofile.close()

            new_file = open(str(output + (file[:file.rfind(".")]) + ".txt"), 'w')
            new_file.write(to_write)
            new_file.close()
        print "Done..."

    @staticmethod
    def process_pdf(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    def process_doxc(self, files):
        self.name = file
        return process(str(files))
