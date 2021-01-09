from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF

import spacy
from svglib.svglib import svg2rlg

def pdf_setting(file_name):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    pdfmetrics.registerFont(TTFont("malgun", "malgun.ttf")) # 한글폰트 사용을 위해 필수
    
    base_canvas = canvas.Canvas(file_name)                  # 파일이름 세팅
    base_canvas.setPageSize((11*72, 8.5*72))                # A4 가로 방향, inch -> dot
    
    return base_canvas   

def draw_spacy_doc(my_canvas, sentence):
    doc = nlp(source)
    svg = spacy.displacy.render(doc, style="dep")

    temp = open("a.svg", 'w', encoding ='utf-8')
    temp.write(svg)
    temp.close()

    temp = open("a.svg", "r", encoding ='utf-8')
    drawing = svg2rlg(temp)
    temp.close()
    
    renderPDF.draw(drawing, my_canvas, 0, 200)
    
def make_page(my_canvas, source, target):
    my_canvas.setFont("malgun", 14)
    my_canvas.drawString(650, 580, '파이썬 자연어처리')
    my_canvas.drawString(650, 560, '중3 영어 Lessson2')

    my_canvas.drawString(390, 20, '- ' + str(i+1) + ' -')

    origin_sentence = "원문 : " + source
    my_canvas.drawString(50, 495, origin_sentence.encode("utf-8"))
    draw_spacy_doc(my_canvas, source)

    my_canvas.setFillColorRGB(0.8,0,0)
    transe_sentence = "번역 : " + target
    my_canvas.drawString(50, 470, transe_sentence.encode("utf-8"))
    
    my_canvas.showPage()

if __name__ == "__main__":
    c = pdf_setting("hello.pdf")
    nlp = spacy.load("en_core_web_sm")

    f = open("test.txt", "r", encoding ="utf-8")
    for i in range(3):
        source = f.readline().replace("\n", "")
        target = f.readline().replace("\n", "")
        make_page(c, source, target)

    c.save()
    f.close()
