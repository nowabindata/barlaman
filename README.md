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
 
 

                    




