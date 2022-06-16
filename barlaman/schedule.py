import pdfplumber
from bidi.algorithm import get_display
import arabic_reshaper
import re
from .utils import getPage,getRawFP,getRawF2Table,getLignsF2Table


def getSchedule(path):
    '''
    > Get ready-to-use data of the first two tables of the schedule pdf file (ordre_de_jour_DDMMYYYY)
      It outputs a dictionary  with the following keys :
       ++ "President": The president of the session
       ++ "nbrQuestTotalSession" : Total nbr of questions
       ++ "Ministries" :  "nomsMinister" : Name of ministers present in the session
                          "numsQuest" : Total Number of question per minister
                          "numQuestU": Number of urgent (أنى)  question
       ++ "Groups":  "nomsGroup" : Parliament groups
                     "quesTime": Time allocated for each group
                     "addTime" : Time for additional comments
    > params :
        - path : path to pdf
    '''
    presid=[]
    nbrQuestTotalSession=[]
    numsQuest=[]
    numQuestU=[]
    nomsGroup=[]
    quesTime=[]
    addTime=[]
    nomsMinister=[]
    F2Table=getRawF2Table(path)
    try :
        tab=getLignsF2Table(F2Table[1])
    except:
        tab=getLignsF2Table(F2Table)
        
    for i in range(len(F2Table)) :
        if i!=1:
            prv=getLignsF2Table(F2Table[i])
            for j in range(len(prv)):
                tab[j]+=prv[j]
    if tab[0]!=[]:
        presid=tab[0]
        nbrQuestTotalSession=tab[1]
    nomsGroup=[name[0] for name in tab[2] if name!=[] ]
    quesTime=[name[0] for name in tab[3] if name!=[] ]
    try :
        addTime=[name[1] for name in tab[3] if name!=[] ]
    except :
        addTime=[]
    numsQuest=[int(num[0]) for num in tab[-1] if len(num)>1]
    numQuestU=[int(num[1]) for num in tab[-1] if len(num)>1]
    
    if nbrQuestTotalSession!= [] and sum(numsQuest)!=int(nbrQuestTotalSession[0]):
        numsQuest=numsQuest[:-1]
    nomsMinister=[name[0] for name in tab[-2] if name!=[]]
    while len(nomsMinister)!=len(numsQuest):
        nomsMinister[-2]=nomsMinister[-2] + ' ' +nomsMinister[-1]
        nomsMinister=nomsMinister[:-1]
    return {"President":presid,
            "nbrQuestTotalSession" :nbrQuestTotalSession,
            
            "Ministries":{"nomsMinister" : nomsMinister,
            "numsQuest" : numsQuest,
            "numQuestU":numQuestU},
            "Groups":{"nomsGroup" : nomsGroup,
            "quesTime": quesTime,
            "addTime" : addTime
            }}