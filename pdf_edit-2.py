#pdf_merger.py
#from PyPDF2 import PdfFileReader, PdfFileWriter

import os
import glob
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path, convert_from_bytes

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}_page_{}.pdf'.format(fname, page+1)

        with open('./temp/'+output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()

    for path in input_paths:
        pdf_reader = PdfFileReader('./temp/'+path)
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            #page.rotateClockwise(270)
            print(page.extractText())
            
            pdf_writer.addPage(page)

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

def to_jpg(file_name) :
    path = r'C:\Program Files\poppler\bin'

    images = convert_from_path(file_name, dpi = 300, poppler_path=path)
    temp_name = file_name[:len(file_name)-4]
    
    for i in range(len(images)):
        images[i].save(f"./temp/{temp_name}_{i}.jpg")
        
if __name__ == '__main__':

    os.makedirs('./temp', exist_ok=True)
    
    # pdf 파일 페이지 단위로 분할하기
    #file_name = input("편집 대상 pdf 파일명을 입력하시오(확장자 포함) : ")

    file_name = "string.pdf"
    '''
    pdf_merge_list = []
    firs_page = 1
    last_page = 3
    for i in range(firs_page, last_page+1):
        merge_file_name = file_name_pre + "_page_" + str(i) + '.pdf'
        pdf_merge_list.append(merge_file_name)
    '''

    try:
        pdf_splitter(file_name)
    except FileNotFoundError as file_err:
        print("입력한 pdf 파일을 찾을 수 없습니다.")
        sys.exit()
    
    # 특정 페이지만 지정해서 합치기 할 경우
    
    #pdf_merge_list_raw = ['10~17', '18~42', '44~61', '62~80', '82~98']
    #pdf_merge_list_raw_total = [['2~22'], ['24~40'], ['42~69'], ['70~89'], ['90~107'], ['108~127']]
    pdf_merge_list_raw_total = [['1~13']]
    
    #pdf_merge_list_raw = ['82~98']

    for cnt in range(len(pdf_merge_list_raw_total)):
        pdf_merge_list_raw = pdf_merge_list_raw_total[cnt]
        
        pdf_merge_list_num = [ ]
        for i in range(len(pdf_merge_list_raw)):
            print('리스트 분석....', pdf_merge_list_raw[i])
            if '~' in str(pdf_merge_list_raw[i]):
                list_anal = pdf_merge_list_raw[i].split('~')
                for j in range(int(list_anal[0]), int(list_anal[1])+1):
                    print(j)
                    pdf_merge_list_num.append(j)
            else:
                print(pdf_merge_list_raw[i])
                pdf_merge_list_num.append(pdf_merge_list_raw[i])

        pdf_page_num = PdfFileReader(file_name).getNumPages()
        
        if (pdf_merge_list_num[-1] > pdf_page_num):
            print(f"{file_name} 페이지 수 : {pdf_page_num}, 입력하신 페이지 번호 초과")
            sys.exit()
        
        # 페이지 범위를 지정해서 합치기 할 경우
        """
        firs_page = 1
        last_page = 3
        for i in range(firs_page, last_page+1):
            pdf_merge_list_num.append(i)
        """

        # 분할된 pdf 원하는 페이지만 합치기
        file_name_pre = file_name.split('.')[0]
        #pdf_merge_list = glob.glob(f'{file_name_pre}_*.pdf')
        #pdf_merge_list.sort()
        
        pdf_merge_list = []
        for i in range(len(pdf_merge_list_num)):
            merge_file_name = file_name_pre + "_page_" + str(pdf_merge_list_num[i]) + '.pdf'
            pdf_merge_list.append(merge_file_name)
            
        merger(f'{file_name_pre}_merge_result{pdf_merge_list_raw_total[cnt]}.pdf', pdf_merge_list)
