# PyMuPDF 패키지 불러오기
import fitz  
import glob
import os
import shutil
import pandas as pd

############# src_path 파일들의 확장자 변경(복사) #############
def rename_file_ext(src_path, des_ext)  :
    files = glob.glob(src_path)
    
    for src_filename in files:
        #print(f"{src_filename} 처리중....")
        pre, ext = os.path.splitext(src_filename)
        des_filename = pre + des_ext
        
        if des_filename in files:
            print(f"{des_filename}은 이미 존재합니다")
        else:
            shutil.copy(src_filename, des_filename)

    files = glob.glob(os.path.dirname(src_path) + "/*" + des_ext)
    
    return files

############# table들을 DataFrame으로 변환하기 #############
def tables_to_dfs(tables):
    dfs = []
    for table in tables:
        df = table.to_pandas() 
        cols = [col_name.replace("\x01", "") for col_name in df.columns]  #특수문자 제거
        df.columns = cols

        for i in range(len(df)):
            for j in range(len(df.columns)):
                if type(df.iloc[i,j]) == str:
                      #print(df.iloc[i,j])
                      df.iloc[i,j] = df.iloc[i,j].replace("\x01", "")    #특수문자 제거
                      
        print(df)
        dfs.append(df)

    return dfs

############# DataFrame들을 엑셀 파일에 저장 #############
def dfs_to_excel(dfs, filename):
    startrow = 0
    with pd.ExcelWriter(filename) as writer:
        for df in dfs:
            df.to_excel(writer, engine="xlsxwriter", startrow=startrow)
            startrow += (df.shape[0] + 2)

########### 형광펜으로 특정 키워드 표시하기  ###########
def highlight_text_in_pdf(pdf_document, output_pdf_path, search_text, rgb):
    cnt = 0
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        matches = page.search_for(search_text)

        for match in matches:           
            highlight = page.add_highlight_annot(match)
            highlight.set_colors(stroke=rgb)   
            highlight.update()
            
            cnt = cnt +1
            
    pdf_document.save(output_pdf_path)

    return cnt

#########################################################
#########################################################
#########################################################

files = rename_file_ext("samples/*.p", ".pdf")
input_pdf_path = "./samples/화장품.pdf"  

with fitz.open(input_pdf_path) as pdf_doc:
    highlight_keyword = "화장품"
    cnt = highlight_text_in_pdf(pdf_doc, "형광펜_표시.pdf", highlight_keyword, (1, 1, 0))  #노란색
    print(f"{input_pdf_path}파일에 {highlight_keyword} {cnt}개의 형광펜 표시 완료\n")

    highlight_keyword = "수출"
    cnt = highlight_text_in_pdf(pdf_doc, "형광펜_표시.pdf", highlight_keyword, (1, 0, 0))  #빨간색
    print(f"{input_pdf_path}파일에 {highlight_keyword} {cnt}개의 형광펜 표시 완료\n")
    
    
    tables = pdf_doc.load_page(13).find_tables()
    dfs = tables_to_dfs(tables)
    dfs_to_excel(dfs, "표(table)_추출.xlsx")
    

#########################################################
#########################################################
#########################################################
