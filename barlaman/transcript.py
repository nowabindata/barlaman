import pdfplumber
from bidi.algorithm import get_display
import arabic_reshaper
import re
import json
import os
from .utils import storeJSON,storeTXT,createDir,storeAllJSON,storeAllTXT

def getRawTrscp(path,start=1,end=-1,two_side=True):
    '''
    > Get the raw text of the transcript
    > It returns a dictionary of dictionaries in the form of :
       {'page_1':{"page":page,"rigth":right,"left":left}}
       where : - page_1: page number (e.g.page_x is page number x)
               - page : the text of page_1
               - right : the text of the right side of page_1
               - left : the text of the left side of page_1
    > params :
        - path: pdf path
        - start (default =1) : The number of the page from where you want to begin extracting text.
                               The first page is 1 not 0!
        - end (default=-1) : The number of the page to where you want to stop extracting text
        - two_side=True : if the pdf has two sides one in the left and the other in the right
    
    '''
    if two_side==False :
        with pdfplumber.open(path) as pdf:
            text=dict()
            if end==-1:
                end=len(pdf.pages)
            for pgNbr in range(start-1,end):
                page = pdf.pages[pgNbr]
                txt=page.extract_text()
                bidi_text = get_display(txt)
                reshaped_text = arabic_reshaper.reshape(bidi_text)
                text['_'.join(['page',str(pgNbr+1)])]={'page':reshaped_text}
        
    else :
        with pdfplumber.open(path) as pdf:
            x0 = 0    # Distance of left side of character from left side of page.
            x1 = 0.5  # Distance of right side of character from left side of page.
            y0 = 0  # Distance of bottom of character from bottom of page.
            y1 = 0.9  # Distance of top of character from bottom of page.
            text=dict()
            if end==-1:
                end=len(pdf.pages)
            for pgNbr in range(start-1,end):
                page = pdf.pages[pgNbr]
                left=page.crop((x0*float(page.width),y0*float(page.height),x1*float(page.width),y1*float(page.height)))
                page_text_left=left.extract_text()
                bidi_text_left = get_display(page_text_left)
                reshaped_text_left = arabic_reshaper.reshape(bidi_text_left)
                right=page.crop((0.5*float(page.width), y0*float(page.height), 1*float(page.width), y1*float(page.height)))
                page_text_right=right.extract_text()
                bidi_text_right = get_display(page_text_right)
                reshaped_text_right = arabic_reshaper.reshape(bidi_text_right)
                page_text = '\n'.join([reshaped_text_right, reshaped_text_left])
                text['_'.join(['page',str(pgNbr+1)])]={
                    "page":page_text,
                    "right":reshaped_text_right,
                    "left":reshaped_text_left}
    return text


def texToDir(path_pdf,parent_dir,start=1,end=-1,two_side=True,both_format=True,file_type='json'):
    '''
    > Create a directory to store files 
    > params :
        - path_pdf : pdf path
        - parent_dir : directory where to create a directory to store data
        - start (default=1): Number of the page from where you want to begin extracting text.
                               The first page is 1 not 0!
        - end (default=-1) : Number of the page to where you want to stop extracting text
        - both_format (default=True) :True if you want to store file in json AND txt format.
                                   If it's False, you may sepecify format with file_type
        - file_type (default ='json') : json or txt. It both_format= True, you don't need to use this parameter
        - two_side=True : if the pdf has two sides one in the left and the other in the right
    '''
    text=getRawTrscp(path_pdf,start,end,two_side)
    print("Text parsing completed")
    file_name=path_pdf.split('/')[-1].replace('.pdf','')
    path_dir=createDir(parent_dir,file_name)
    print("Directory ceated")
    if both_format==True:
        storeAllJSON(file_name,path_dir,text)
        print("JSON file created")
        storeAllTXT(path_dir,text,file_name)
        print("Text files created")
    else :
        if file_type=='json':
            storeAllJSON(file_name,path_dir,text)
            print("JSON files created")
        else :
            storeAllTXT(path_dir,text,file_name)
            print("Text files created")