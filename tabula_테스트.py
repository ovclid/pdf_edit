#pip install tabula-py  (not tabula)
#pip3 install jpype1
#java 설치

import tabula
import glob
import os
import shutil

############# src_path 파일들의 확장자 변경(복사) #############
def rename_samples(src_path, des_ext)  :
    files = glob.glob(src_path)
    
    for src_filename in files:
        print(f"{src_filename} 처리중....")
        pre, ext = os.path.splitext(src_filename)
        des_filename = pre + des_ext
        
        if des_filename in files:
            print(f"{des_filename}은 이미 존재합니다")
        else:
            shutil.copy(src_filename, des_filename)

    files = glob.glob(os.path.dirname(src_path) + "/*" + des_ext)
    
    return files

##########################################################
##########################################################
##########################################################
files = rename_samples("samples/*.p", ".pdf")
dfs = tabula.read_pdf(files[0], pages = 14)
