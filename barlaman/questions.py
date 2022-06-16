import pdfplumber
from bidi.algorithm import get_display
import arabic_reshaper
import re
from .utils import getRawQuests, getLignQuests,cleanHB,testHB



def getQuesTable(path):
    '''
    > Get question tables
    > It returns a dictionary of dictionaries whose keys are the the names of  ministeries present at the setting.
      Inside of each dictionary there is a dictionary with the following keys :
         - "timeQuest": Time allocated for each question
         - "parlGroup": Parliamentary group
         - "txtQuest": The question,
         - "typeQuest": Question type
         - "codeQuest": Question code
         -  "indexQuest": Question index (order)
         - "subjIden":questions with the same subjIden means the the questions have the same subject (identical subject)(e.g. وحدة الموضوع)
    > params :
       - path : pdf path
    '''
    text=getLignQuests(path)
    idx=[]
    for i in range(len(text)):
        if re.search('ﺭﻗﻢ ﺍﻟﺴﺆﺍﻝ   ﻧﻮﻉ ﺍﻟﺴﺆﺍﻝ   ﻣﻮﺿﻮﻉ ﺍﻟﺴﺆﺍﻝ   ﺍﻟﻔﺮﻳﻖ ﺍﻟﻨﻴﺎﺑﻲ',text[i])!=None :
            idx.append(i)
    idx.append(len(text)+1)
    id=0
    tab=dict()
    while id < (len(idx)-1):
        minister=text[idx[id]-1]
        ligns=text[idx[id]+1:idx[id+1]-1]
        id+=1
        subjIden=[]
        indexQuest=[]
        codeQuest=[]
        typeQuest=[]
        txtQuest=[]
        parlGroup=[]
        timeQuest=[]
        for i in range(len(ligns)):
            
            if re.search(r'\d\d:\d\d:\d\d',ligns[i])==None:
                txtQuest[-1]=txtQuest[-1]+' '+ligns[i]
                continue;
            ligns[i]=ligns[i].replace('ﻓﺮﻳﻖ'," ﻓﺮﻳﻖ").replace("ﺍﻟﻔﺮﻳﻖ"," ﺍﻟﻔﺮﻳﻖ").replace("ﺍﻟﻤﺠﻤﻮﻋﺔ"," ﺍﻟﻤﺠﻤﻮﻋﺔ")
            vals=ligns[i].split('  ')
            vals=[val.strip() for val in vals if val.strip()!='']
            if vals[0][0]=='*':
                subjIden.append(vals[0])
                vals=vals[1:]
            else :
                subjIden.append(' ')
            indexQuest.append(vals[0])
            typeQuest.append(vals[2])
            txtQuest.append(vals[3])
            parlGroup.append(vals[4])
            try :
                timeQuest.append(vals[5])
            except :
                timeQuest.append(' ')
            if ' ' in vals[1]:
                codeQuest.append(vals[1][-1]+vals[1][:-1])
            else :
                codeQuest.append(vals[1])
        tab[minister]={"timeQuest": timeQuest,
                   "parlGroup": parlGroup,
                   "txtQuest": txtQuest,
                   "typeQuest": typeQuest,
                   "codeQuest": codeQuest,
                   "indexQuest": indexQuest,
                   "subjIden":subjIden}
    return tab