from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

file_name = "string_.pdf"
# read your existing PDF
existing_pdf = PdfFileReader(open(file_name, "rb"))
pages = existing_pdf.getNumPages()
print(pages)

temp_pdf_writer = PdfFileWriter()
can = canvas.Canvas(f"temp_canvas.pdf", pagesize=letter)

for i in range(pages):
    #packet = io.BytesIO()
    can.drawString(300, 10, f"{i+1}")

    """
    if i == 0:
        can.setFillColorRGB(1,1,1)
        can.rect(10,300,550,780,fill = 1, stroke=0)
        
    elif i == pages-1 :
        can.setFillColorRGB(1,1,1)
        can.rect(10,30,550,400,fill = 1, stroke=0)
    """    
    can.showPage()

can.save()

new_pdf = PdfFileReader("watermark.pdf")

output = PdfFileWriter()
for i in range(pages):
    print(i)
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(i))
    #page.compressContentStreams()
    output.addPage(page)


outputstream = open("watermark.pdf", "wb")
output.write(outputstream)
outputstream.close()
