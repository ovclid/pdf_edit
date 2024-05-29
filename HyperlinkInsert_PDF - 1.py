from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import shutil
import pandas as pd
import os, sys

######### 파일 준비 및 분석하기 (링크정보 파일, PDF 파일 2개 필요)  ###############
print("\n-----------------------------------------------------------------")
link_info_file = "Hyperlink_info.txt"
if os.path.exists(f"./{link_info_file}"):
    print(f"{link_info_file} 파일 정보 분석중....")
    link_info = pd.read_csv(link_info_file)
    print(link_info)
else:
    print(f"{link_info_file} 존재하지 않아 프로그램을 종료합니다.")
    sys.exit()

print("\n-----------------------------------------------------------------")
pdf_file_name = "중기누리.p"
if os.path.exists(f"./{pdf_file_name}"):
    print(f"{pdf_file_name} pdf 파일로 전환 및 분석중...")
    shutil.copy(pdf_file_name, "중기누리.pdf")

    pdf_file = open("중기누리.pdf", "rb")
    pdf_reader = PdfReader(pdf_file)
    pages = len(pdf_reader.pages)
    print(f"총 페이지 수 : {pages}")
    box = pdf_reader.pages[0].mediabox
    print(f"가로 : {int(box.width)}cm, 높이 : {int(box.height)}cm")
else:
    print(f"{pdf_file_name} 파일이 존재하지 않아 프로그램을 종료합니다.")
    sys.exit()
print("\n-----------------------------------------------------------------")

########### 임시 캔버스 pdf에 하이퍼링크 만들기 #################
can = canvas.Canvas("temp_canvas.pdf", pagesize = (box.width, box.height))
answer = input("링크 영역을 사각형으로 표시 할까요? (y/n) ")
      
#x, y = 20, int(box.height - 150)
x, y = 30, 30
width, height = int(box.width) - 60 , 220

for i in range(pages):
    print(f"{i+1} 페이지 처리중...")
    for j in range(len(link_info)):
        if link_info["page"][j] == i+1:  
            #can.drawString(link_info["x"][j], link_info["y"][j], "hello")
            hyperlink_pos = (link_info["x"][j],
                                    link_info["y"][j],
                                   link_info["x"][j]+link_info["너비"][j],
                                   link_info["y"][j]+link_info["높이"][j])                                   

            #can.setFillColorRGB(1, 1, 0)
            if answer.upper()  == "Y":  # 사각형 그리기
                can.rect(hyperlink_pos[0], hyperlink_pos[1], hyperlink_pos[2] - link_info["x"][j], hyperlink_pos[3] -link_info["y"][j], stroke = 1, fill=0)
        
            link = link_info["사이트"][j]
            can.linkURL(link, hyperlink_pos, color =0x000000, relative = 0 )
            print(f"{i+1} 페이지 {link} 처리완료")
    can.showPage()
can.save()

######## 임시 캔버스 pdf와 기존 pdf파일 합쳐서 최종 파일로 저장 ########
new_pdf = PdfReader("temp_canvas.pdf")
output = PdfWriter()
for i in range(pages):
    page = pdf_reader.pages[i]

    page.merge_page(new_pdf.pages[i])
    #new_pdf.pages[i].merge_page(page)
    
    output.add_page(page)
    #output.add_page(new_pdf.pages[i])

if answer.upper()  == "Y":
    outputstream = open("최종 결과_사각형 표시.pdf", "wb")
else:
    outputstream = open("최종 결과_사각형 미표시.pdf", "wb")
output.write(outputstream)
outputstream.close()
