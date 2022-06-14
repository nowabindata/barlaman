from bs4 import BeautifulSoup 
import requests
import json
import re
import importlib.resources
from .utils import getDepdecs,getDepTasks,getDepName,getDepAgenda,getQuestPage,getDepQuest,getQuestDt

def getUrls():
    '''
    Get deputy urls for scrapping
    
    '''
    pages=['']+['='.join(["?page",str(i)]) for i in range(1,33)]
    url_prfx="https://www.chambredesrepresentants.ma/fr/%D8%AF%D9%84%D9%8A%D9%84-%D8%A3%D8%B9%D8%B6%D8%A7%D8%A1-%D9%85%D8%AC%D9%84%D8%B3-%D8%A7%D9%84%D9%86%D9%88%D8%A7%D8%A8/2021-2026"
    urls=dict()
    for page in pages:
        url=''.join([url_prfx,page])
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        divs=soup.find_all('div',class_="woman-slider-content")
        for div in divs:
            span=div.find_all('span')
            dep_name=span[0].text.strip()
            dep_url=span[0].find('a',href=True)["href"]
            urls[dep_name]=''.join(["https://www.chambredesrepresentants.ma",dep_url])
    return urls


def getUrlByName(name):
    '''
    Get Deputy url by name.
    '''
    path=importlib.resources.open_text("barlaman.data", "urls.json").name
    urls=open(path)
    depUrls=json.load(urls)
    urls.close
    name=name.strip()
    if name in depUrls:
        return depUrls[name]
    else :
        return None



def getDeputy(url,include_quest=True,quest_link=False,quest_det=False):
    '''
    > Scrap the web page of a deputy
    >params :
           - url : link to the deputy link
           - include_quest (default=True): True to retuen questions
           - quest_link (default=False) True to include links of each question
           - quest_det(default=False) = True to include question details
    return a dictionary :
          {"Nom":name,"description":desc, "task":task,"Agenda":agenda,"Questions":Quests}
    '''
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ## Deputy name
    name=getDepName(soup)
    ## Description
    desc=getDepdecs(soup)
    ##Parliamentary tasks
    task=getDepTasks(soup)
    ## Deputy agenda
    agenda=getDepAgenda(soup)
    ## Deputy Quest
    Quests=[]
    if include_quest==True:
        Quests=getDepQuest(url,quest_link,quest_det)
    return {"Nom":name,"description":desc, "task":task,"Agenda":agenda,"Questions":Quests}