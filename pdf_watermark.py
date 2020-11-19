from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# read your existing PDF
existing_pdf = PdfFileReader(open("datacamp_1.pdf", "rb"))
pages = existing_pdf.getNumPages()

temp_pdf_writer = PdfFileWriter()

for i in range(pages):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #can.drawString(300, 10, f"{i+1}")
    can.setFont('Times-Roman', 35)
    can.drawString(960, 30, f"{i+1}")
    can.save()

    
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    first_page = new_pdf.getPage(0)
    temp_pdf_writer.addPage(first_page)

    del can
    

output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
for i in range(pages):
    page = existing_pdf.getPage(i)
    page.mergePage(temp_pdf_writer.getPage(i))
    output.addPage(page)
    
# finally, write "output" to a real file
outputStream = open(f"destination{pages}.pdf", "wb")
output.write(outputStream)
outputStream.close()
