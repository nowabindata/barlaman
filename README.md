# Welcome to barlaman
**A Python library to Scrap  raw data from the  Moroccan Parliament (House of Representatives) website.**

## Requirements
These  following packages should be installed:

 + ***BeautifulSoup*** & ***requests*** for web scrapping
 + ***pdfplumber*** for pdf scrapping
 + ***arabic_reshaper*** & ***python-bidi*** to work with arabic text
 + ***re*** for regular expressions.
 + ***json*** & ***os*** to work with JSON files and folders.
## Install (NOT YET)
```python
pip install 
```
## Running the scraper

### I. Scrape the schedule :
Each Monday, and in accordance with the  Constitution, the House of Representatives  convene in a plenary sitting devoted to oral questions. Before the sitting, the House of Representatives publishes the schedul of the sitting (pdf file in arabic). The first page of this document (the schedule) contains the following  data (see picture bellow) :

   + Time allocated to parliamentary groups
   + Ministries invited to the sitting
 
   ***Illustration***
  
![F2tables](https://user-images.githubusercontent.com/49843367/173394096-8c4a5c67-4f91-47c4-9bc2-72c1f0cca76b.png)

To get the schedule use the function : `getSchedule(path)` where `path` is the document path
```python
path= ".../ordre_du_jour_30052022-maj_0.pdf"
schedual = getSchedule(path)
```
The output `schedual` is  a tuple of 3  dictionary with the following keys :
     
+ Dict 1 :
    + "President": The president of the session
    + "nbrQuestTotalSession" : Total nbr of questions
+ Dict 2 :
    +  "nomsMinister" : Name of ministers present in the session
    +  "numsQuest" : Total Number of question per minister
    +  "numQuestU": Number of urgent (أنى)  question
+ Dict 3 :
    + "nomsGroup" : Parliament groups
    + "quesTime": Time allocated for each group
    + "addTime" : Time for additional comments

We can store these dictionaries into DataFrames :
```python
# Turn Dict 2 into a DataFrame
import pandas as pd
pd.DataFrame(schedual[1])
```

### II. Scrape sitting's questions :
The remaining pages of the schedule document contains :
  + Number of questions for each Ministry
  + Questions asked during the sitting, who asked these questions and time allocated to each question

 ***illustration**
 
 ![questTable](https://user-images.githubusercontent.com/49843367/173398931-82a871a8-4cfb-46c9-90fb-a6699d311428.png)
 
 To get these question tables  use the function : `getQuesTable(path)` where `path` is the document path
```python
path= ".../ordre_du_jour_30052022-maj_0.pdf"
question = getQuesTable(path)
```
The output `question` is a dictionary of dictionaries whose keys are the the names of  ministeries present at the setting.Inside of each dictionary there is a dictionary with the following keys :

   - "timeQuest": Time allocated for each question
   - "parlGroup": Parliamentary group
   -  "txtQuest": The question
   -   - "typeQuest": Question type
   -   "codeQuest": Question code
   -   "indexQuest": Question index (order)
   -   "subjIden":questions with the same subjIden means the the questions have the same subject (identical subject)(e.g. وحدة الموضوع)

  ***Example***
 ```python
{
  'ﺍﻟﻌﺪﻝ': {'timeQuest': ['00:02:00', '00:02:00', '00:01:40', '00:01:35'],
  'parlGroup': ['ﻓﺮﻳﻖ الأﺼﺎﻟﺔ ﻭ ﺍﻟﻤﻌﺎﺻﺮﺓ',
   'ﻓﺮﻳﻖ الأﺼﺎﻟﺔ ﻭ ﺍﻟﻤﻌﺎﺻﺮﺓ',
   'ﺍﻟﻔﺮﻳﻖ الاﺸﺘﺮﺍﻛﻲ',
   'ﺍﻟﻔﺮﻳﻖ الاﺴﺘﻘﺎﻟﻠﻲ ﻟﻠﻮﺣﺪﺓ ﻭ ﺍﻟﺘﻌﺎﺩﻟﻴﺔ'],
  'txtQuest': ['ﺗﻮﻓﻴﺮ ﺍﻟﺘﺠﻬﻴﺰﺍﺕ ﺍﻟﻀﺮﻭﺭﻳﺔ ﺇﻟﻨﺠﺎﺡ ﻋﻤﻠﻴﺔ ﺍﻟﻤﺤﺎﻛﻤﺔ ﻋﻦ ﺑﻌﺪ',
   'ﺗﻨﻔﻴﺬ الأﺤﻜﺎﻡ ﺍﻟﻘﻀﺎﺋﻴﺔ ﺿﺪ ﺷﺮﻛﺎﺕ ﺍﻟﺘﺄﻣﻴﻦ',
   'ﺧﻄﻮﺭﺓ ﻧﺸﺮ ﻭﺗﻮﺯﻳﻊ ﺻﻮﺭ الأﻄﻔﺎﻝ ﺃﻭ ﺍﻟﻘﺎﺻﺮﻳﻦ',
   'ﺇﺷﻜﺎﻟﻴﺔ ﺍﻟﺒﻂﺀ ﻓﻲ ﺇﺻﺪﺍﺭ الأﺤﻜﺎﻡ ﺍﻟﻘﻀﺎﺋﻴﺔ'],
  'typeQuest': ['ﻋﺎﺩﻱ', 'ﻋﺎﺩﻱ', 'ﻋﺎﺩﻱ', 'ﻋﺎﺩﻱ'],
  'codeQuest': ['1505 ', '2386 ', '2413 ', '2829 '],
  'indexQuest': ['22', '23', '24', '25'],
  'subjIden': [' ', ' ', ' ', ' ']}
}
 ``` 
 
### III. Setting's transcript
After a setting, the Parliament published a pdf file of the setting transcript in arabin containing all debates that took place during the setting.
The unique content, structure and language of records of parliamentary debates make them an important object of study in a wide range of disciplines in social sciences(political science) [Erjavec, T., Ogrodniczuk, M., Osenova, P. et al. The ParlaMint corpora of parliamentary proceedings] and  computer science (Natural language processing NLP) . 

***Illustration : Transcript***

 ![transcript](https://user-images.githubusercontent.com/49843367/173420355-83d189be-e6b7-4a58-8654-830f8bf1630d.png)

Unfortunatily we can't use the transcript document as it is provided by the parliament website because the document is written with a special font. In fact, if we try to scrape the original document we get a text full of mistakes (characters not in the right order).So we must change document's font before using it.  See the picture bellow : 
  + text in  top is the original document.
  + text in  bottom left is when we scrape the original document 
  + text in  bottom right is when we scrape the original document after we  changed its font

![font](https://user-images.githubusercontent.com/49843367/173423139-e745b517-b1fa-4e15-a8ad-124eb730ec37.png)

Until now there is no pythonic way to change the font of the document  (at least we are not aware of its existence,especialy that it's in arabic. All suggestions are most welcome). So we are doing the the old way : using  Microsoft Word.

To get the raw transcripts  use the function : `getRawTrscp(path,start=1,end=-1)` where `path` is the document path, `start` is the number of the page from where you want to begin extracting text (The first page is 1 not 0!) and `end` is number of the page where you want to stop extracting text.
```python
path=".../42-cdr23052022WF.pdf"
transcript=getRawTrscp(path)
```
The output is a dictionary of dictionaries in the form of : {.,'page_x':{"page":page,"rigth":right,"left":left},.}

where : 
  - page_1: page number (e.g.page_x is page number x)
  - page : the text of page_1
  - right : the text of the right side of page_x
  - left : the text of the left side of page_x

### IV. Deputy data and parliamentary activities
Each deputy has a section at the parliament website where we can find the following data :
  
  + General info about the deputy : Name, Party, Group, District ...
  + Parliamentary tasks: 
  + Deputy Agenda: 
  + Deputy Questions: Total number of questions and for each question we can find the folliwing details :
                           + Question date
                           + Question id
                           + Question title
                           + Question status : if the question received a response  
                           + Date Answer
                           + Question text 

                       

    
                    




