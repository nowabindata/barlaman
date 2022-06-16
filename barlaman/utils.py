import pdfplumber
from bidi.algorithm import get_display
import arabic_reshaper
import re
from bs4 import BeautifulSoup 
import requests
import json
import os


## Utils functions for .schedule
def getPage(path,nopg):
    '''
    > Get Raw text of the page nopg
    > parms:
       - path : the path to the pdf
       - nopg : the Number Of the Page
    
    '''
    # nopg number of page
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[nopg]
        page_text=page.extract_text()
        bidi_text = get_display(page_text)
        reshaped_text = arabic_reshaper.reshape(bidi_text)
    return reshaped_text
def getRawFP(path):
    '''
    > Get Raw text of Page 0 and split the text to 3 parts
    > params :
          - path : the path to the pdf
    '''
    text=getPage(path,0)
    text=text.split("\n \n \n")
    return text
def getRawF2Table(path):
    '''
    > Get the Raw text of the first two tables
    > params :
         - path : the path to the pdf
    '''
    text=getRawFP(path)
    txt=text[1].split("\n \n")
    if len(txt)>1:
        return text[1].split("\n \n")
    else :
        i=0
        while i<len(text):
            if i==1:
                i+=1
                continue;
            else :
                txt=text[i].split("\n \n")
                if len(txt)>1:
                    return txt
                else :
                    i+=1


def getLignsF2Table(text):
    '''
    > Clean the raw text of the first two tables (delete unnecessary words) and separate the two tables
      It return a list of :presid (name of the session president),nbrQuestTotalSession (total number of question)
      nomsGroup (name of parliament groups),dursGroup (time allocated for each parliament group),
      nomsMinister (minister name),numsQuest( the number of question per minister)
    > params :
          - text : the output of getRawF2Table()
    '''
    presid=[]
    nbrQuestTotalSession=[]
    dursGroup=[]
    numsQuest=[]
    nomsGroup=[]
    nomsMinister=[]
    if 'www.chambredesrepresentants.ma' in text:
        return [presid,nbrQuestTotalSession,nomsGroup,dursGroup,nomsMinister,numsQuest]
    wordsToDelet=['ﻣﺠﻠﺲ ﺍﻟﻨﻮﺍﺏ', 'ﻗﺴﻢ ﺍﺃﻟﺴﺌﻠﺔ', 'ﺟﻠﺴﺔ ﺭﻗﻢ','ﻣﺼﻠﺤﺔ ﺍﺃﻟﺴﺌﻠﺔ','ﺃﻣﺎﻧﺔ ﺍﻟﺠﻠﺴﺔ','ﺭﺋﺎﺳﺔ ﺍﻟﺠﻠﺴﺔ','ﺍﻟﻜﺘﺎﺑﺔ ﺍﻟﻌﺎﻣﺔ','ﻣﺪﻳﺮﻳﺔ ﺍﻟﻤﺮﺍﻗﺒﺔ ﻭﺍﻟﺘﻘﻴﻴﻢ','ﺍﻟﺴﻨﺔ ﺍﻟﺘﺸﺮﻳﻌﻴﺔ']
    for word in wordsToDelet:
        text=text.replace(word,'')
    regx=[r'\d\d/\d\d/\d\d\d\d',r'\d\d\d\d-\d\d\d\d']
    for reg in regx:
        exprs=re.findall(reg,text)
        if exprs!=[]:
            for expr in exprs:
                text=text.replace(expr,'')
    text=text.replace('ﺍﺃﻟ','الأ').replace('ﺍﺍﻟ','الا').replace('ﺍﺇﻟ','الإ')
    v=text.split("\n")
    w=[ st.rstrip().lstrip()  for st in v if re.search('\d',st)!=None]
    presid=[]
    nbrQuestTotalSession=[]
    dursGroup=[]
    numsQuest=[]
    nomsGroup=[]
    nomsMinister=[]
    gotPresid=False
    for lig in range(len(w)):
        check=['ﻣﻨﻬﺎ']
        if  gotPresid==False and check[0] in w[0] :
            k=w[lig].split('   ')
            presid=[k[0].replace('  ',"")]
            try :
                nbrQuestTotalSession=re.findall(r'\d+',k[1])
            except :
                nbrQuestTotalSession=re.findall(r'\d+',w[lig]) 
            gotPresid=True
            continue;
        a=w[lig].split("  ")
        a=[x.rstrip().lstrip() for x in a]
        durGroup=[]
        for i in range(len(a)):
            prv=re.findall(r"\d\d:\d\d:\d\d",a[i])
            if prv!=[]:
                durGroup+=prv
        for dur in durGroup:
            a.remove(dur)
        #split digits and words
        numQuest=re.findall(r'\d+',' '.join(a))
        if numQuest!=[]:
            if len(a)<2:
                a=[' ']
            else :
                for num in numQuest:
                    a.remove(num)
        if '' in a :
            a.remove('')
        nomGroup=[]
        nomMinister=[]
        check=['ﻓﺮﻳﻖ','ﺍﻟﻔﺮﻳﻖ']+["ﺍﻟﻤﺠﻤﻮﻋﺔ"]+["ﻣﻨﺘﺴﺒﻴﻦ"]
        for i in range(len(a)):
            if check[0] in a[i] or check[1] in a[i] or check[2] in a[i] or check[3] in a[i]:
                nomGroup.append(a[i])
            elif a[i]!='':
                nomMinister.append(a[i])
        nomsGroup.append(nomGroup)
        nomsMinister.append(nomMinister)
        dursGroup.append(durGroup)
        numsQuest.append(numQuest)
    return [presid,nbrQuestTotalSession,nomsGroup,dursGroup,nomsMinister,numsQuest]


## utils for questions
def getRawQuests(path):
    '''
    > Get Raw text of questions
    > params :
       - path : the path to the pdf
    '''
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages[1:]
        page_text=''
        for i in range(len(pages)):
            page_text+=pages[i].extract_text()
        bidi_text = get_display(page_text)
        reshaped_text = arabic_reshaper.reshape(bidi_text)
    return reshaped_text

def getLignQuests(path):
    '''
    > Get cleaned  question ligns : delete the header and the bottom of each page
    > params :
         - path : path to pdf
    '''
    text=getRawQuests(path)
    ligns=text.split("\n")
    ligns==[txt for txt in ligns]
    ligns=[txt.replace('ﺍﺃﻟ','الأ').replace('ﺍﺍﻟ','الا').strip() for txt in ligns ]
    ligns=[ txt for txt in ligns if txt!='']
    ligns=cleanHB(ligns)
    ligns=[lign.replace('ﺍﻟﻨﻮﺍﺏ  ﻏﻴﺮ ﺍﻟﻤﻨﺘﺴﺒﻴﻦ',"ﺍﻟﻨﻮﺍب ﻏﻴﺮ ﺍﻟﻤﻨﺘﺴﺒﻴﻦ") for lign in ligns]
    return ligns

def cleanHB(lgns):
    '''
    > delete the header and the bottom of each page
    > params :
        - lgns (ligns) : question ligne (table ligne)
    '''
    index=0
    lgnsC=[] # ligne Cleaned
    while index<len(lgns):
        if testHB(lgns[index])==False:
            lgnsC.append(lgns[index])
        index+=1
    return lgnsC

def testHB(ligne):
    '''
    > Test if a ligne is a header or the bottom of the page
    > returns a boolean
    '''
    if re.search(r'^ﻣﺠﻠﺲ ﺍﻟﻨﻮﺍﺏ.*\d{2}/\d{2}/\d{4}$',ligne)!=None:
        return True
    elif re.search(r'^ﺍﻟﻮﺍﻟﻴﺔ ﺍﻟﺘﺸﺮﻳﻌﻴﺔ.*\d{4}-\d{4}$',ligne)!=None :
        return True
    elif re.search(r'^ﺩﻭﺭﺓ ﺃﺑﺮﻳﻞ.*\d{4}$',ligne)!=None :
        return True
    elif re.search(r'^ﺍﻟﺠﻠﺴﺔ ﺭﻗﻢ.*\d+$',ligne)!=None:
        return True
    elif re.search(r'^\d+$',ligne)!=None:
        return True
    else:
        return False

## utils for transcript
def storeJSON(path,data):
    '''
    > Store data into a json file located in path
    '''
    if path.endswith('.json')==False :
        print("Add .json to path")
        return 0
    with open(path,'w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False)

def storeTXT(path,data):
    '''
    > Store data into a .txt file located in path
    '''
    if path.endswith('.txt')==False :
        print("Add .txt to path")
        return 0
    with open(path,'w',encoding="utf8") as file :
        file.write(data)
        
def createDir(parent_dir,new_dir):
    '''
    > Create new directory (new_dir) in a parent directory (parent_dir) to store files
    '''
    path=os.path.join(parent_dir,new_dir)
    if os.path.exists(path)==False:
        os.mkdir(path)
    return path

def storeAllJSON(file_name,path_dir,text):
    '''
    > Organize json file in a directory. It creates one json files named with the same name as the pdf file
    '''
    file_json='.'.join([file_name,'json'])
    path_json='/'.join([path_dir,file_json])
    storeJSON(path_json,text)
def storeAllTXT(path_dir,text,file_name):
    '''
    > Organize txt files in a directory. Creates two type of files :
        - page_x : txt file for each page
        - file_name (the name of pdf) :txt file of the entire transcript
    '''
    txt_cp=''
    for key in text.keys():
            txt=text[key]['page']
            file_txt='.'.join([key,'txt'])
            path_txt=path_txt='/'.join([path_dir,file_txt])
            storeTXT(path_txt,txt)
            txt_cp='\n'.join([txt_cp,txt])
    file_txt='.'.join([file_name,'txt'])
    path_txt='/'.join([path_dir,file_txt])
    storeTXT(path_txt,txt_cp)




## utils for deputy
def getDepdecs(soup): 
    '''
    Get Deputy description :party, group, District, legislature ...
    returns a dictionary. 
    '''
    dev=soup.find("div",class_='mhr-b1_info')
    if dev==None :
        return dict()
    tab=dict()
    clas=['mhr-b1-info-l','mhr-b1-info-r']
    for cl in clas :
        side=dev.find('div',class_=cl).find_all('span')
        if len(side) % 2 !=0:
            side=side[:-1]
        i= 0
        vrs=[]
        while i<len(side):
            vr=side[i].text.replace(':','').strip()
            vl=side[i+1].text
            if vr in vrs :
                vr='_'.join([vr,'1'])
                if vr in vrs:
                    vr='_'.join([vr,str(i)])
            tab[vr]=vl
            vrs.append(vr)
            i+=2
    return tab
def getDepTasks(soup):
    '''
    Get Parliamentary tasks of a deputy
    Returns a dictionary
    '''
    dev=soup.find('div',class_='col-md-8 mhr-b2_tasks')
    if dev==None :
        return dict()
    tasks=dev.find_all('li')
    tab=dict()
    for tsk in tasks :
        task=tsk.text.replace('\n','')
        task=task.split(':')
        tab[task[0].strip()]=task[1].strip()
    return tab
def getDepName(soup):
    '''
    Get deputy Name
    '''
    tab=dict()
    dev=soup.find("div",class_='mhr-b1_info')
    if dev==None:
        return dict()
    title=dev.find('h3').text
    title=title.split(':')
    if len(title)>=2 :
        tab[title[0]]=title[1]
    else :
        title=title[0].split(' ')
        tab[title[0]]=' '.join(title[1:])
    return tab
def getDepAgenda(soup):
    '''
    Get the agenda of a deputy
    Returns a dictionary
    '''
    k=soup.text
    
    spn=re.search(r'events: .+ \}\)\;',k,flags=re.DOTALL)
    if spn==None :
        return dict()
    spn=spn.span()
    a=k[spn[0]:spn[1]]
    i=a.split("description")
    agenda=dict()
    for j in range(1,len(i)):
        p=i[j].split('//')
        hspn=re.search(r'\d\d:\d\d',p[0])
        if hspn!=None :
            hspn=hspn.span()
            heur=p[0][hspn[0]:hspn[1]]
            u=re.search(r'\<a.+\<\/a\>',p[0],flags=re.DOTALL)
            if u!=None :
                u=u.group()
                tspn=re.search('".+"',u)
                if tspn!=None :
                    tspn=tspn.span()
                    txt=u[tspn[1]:].replace("</a>",'').replace('>',"")
                    agenda['_'.join(['Agenda',str(j)])]={"heure":heur,"evenemnt":txt}    
    return agenda
def getQuestPage(soup,qlink=False,qDet=False):
    '''
    Get the question of a page
    '''
    dates=[]
    quests=[]
    questrs=[]
    hrefs=[]
    status=[]
    txtQuests=[]
    div=soup.find_all("div",class_='q-block3')
    if div!=[]:
            for i in range(len(div)):
                st=div[i].find("span",class_="q-status q-st-red")
                if st!=None :
                    status.append("NR")
                else :
                    st=div[i].find("span",class_="q-status q-st-green")
                    if st!=None :
                        status.append("R")
                    else :
                        status.append("NS")
                date=div[i].find_all('div',class_="q-b3-col")[0].find_all("div")[1].text.strip()
                quest=div[i].find_all('div',class_="q-b3-col")[0].find_all("div")[0].text.strip()
                if qlink==True or qDet==True  :
                    href=div[i].find_all('div',class_="q-b3-col")[0].find_all("div")[0].find('a',href=True)['href']
                    if qlink==True :
                        hrefs.append(href)
                    if qDet==True:
                        txtQuest=getQuestDt(href)
                        txtQuests.append(txtQuest)
                dates.append(date)
                quests.append(quest)
                
    return (dates,quests,status,hrefs,txtQuests)
def getDepQuest(url,qlink=False,qDet=False):
    '''
    get questions of a deputy
    '''
    urlq='/'.join([url,"questions"])
    reqq = requests.get(urlq)
    soupq = BeautifulSoup(reqq.content, "html.parser")
    div=soupq.find('div',class_='f-result-counter')
    nbrQ=[]
    if div==None:
        return {"NbrQuest":[0]}
    else :
        nbrQ=div.text
        nbrQ=re.findall(r'\d+',nbrQ)
    first=getQuestPage(soupq,qlink,qDet)
    #get the number of  last page:
    div=soupq.find('li',class_='next last')
    if div!=None :
        extp=re.findall(r'page\=\d+',div.find("a",href=True)['href'])[0]
        last=int(re.findall(r'\d+',extp)[0])
        for i in range(1,(last+1)):
            ext='='.join(['page',str(i)])
            url_next='?'.join([urlq,ext])
            req_next = requests.get(url_next)
            soup_next = BeautifulSoup(req_next.content, "html.parser")
            next_=getQuestPage(soup_next,qlink,qDet)
            for j in range(len(next_)):
                first[j].extend(next_[j])
    return {"NbrQuest":nbrQ,"Dates":first[0],"Questions":first[1],"Status":first[2],"Quest_link":first[3],"Quest_txt":first[4]}

def getQuestDt(href):
    '''
    Get question details
    '''
    urlqd=''.join(["https://www.chambredesrepresentants.ma",href])
    req_qd = requests.get(urlqd)
    soup_qd = BeautifulSoup(req_qd.content, "html.parser")
    div=soup_qd.find('div',class_='q-b1-1')
    data=[]
    var=[]
    if div!=None :
        span=div.find_all("span")
        if span!=[]:
            span=[spn.text.strip() for spn in span if spn.text.strip()!='']
            span[-2]=' '.join([span[-2],span[-1]])
            span=span[:-1]
            check=0
            for spn in span:
                lign=spn.split(':')
                if check==0 :
                    check=1
                    lign[0]='Nombre Question'
                var.append(lign[0])
                data.append(lign[1])
        # Question txt
        div_d=soup_qd.find("div",class_='q-b1-3')
        if div_d != None :
            span=div_d.find_all("div")
            if span!=None :
                for spn in span:
                    sp=spn.text.strip().replace('\n','').split(":")
                    var.append(sp[0].strip())
                    data.append(sp[1].strip())
    return dict(zip(var,data))