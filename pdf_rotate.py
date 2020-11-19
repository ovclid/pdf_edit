import os
import glob
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader

pdf_filename = '진료비.pdf'

pdf_in = open(pdf_filename, 'rb')
pdf_reader = PdfFileReader(pdf_in)
pdf_writer = PdfFileWriter()

for i in range(pdf_reader.numPages):
	page = pdf_reader.getPage(i)
	page.rotateClockwise(90)
	pdf_writer.addPage(page)

pdf_out = open(f'{pdf_filename}_ratated.pdf', 'wb')
pdf_writer.write(pdf_out)

pdf_out.close()
pdf_in.close()
