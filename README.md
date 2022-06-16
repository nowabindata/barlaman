# Welcome to barlaman
**A Python library to Scrap  raw data from the  Moroccan Parliament (House of Representatives) website.**

 + PyPI link : https://pypi.org/project/barlaman/

## Requirements
These  following packages should be installed:

 + ***BeautifulSoup*** & ***requests*** for web scrapping
 + ***pdfplumber*** for pdf scrapping
 + ***arabic_reshaper*** & ***python-bidi*** to work with arabic text
 + ***re*** for regular expressions.
 + ***json*** & ***os*** to work with JSON files and folders.
 + ***importlib*** to access the data about deputy url.
## Install 
```python
pip install barlaman
from barlaman import *
```
## Running the scraper

### I. Scrape the schedule :
Each Monday, and in accordance with the  Constitution, the House of Representatives  convene in a plenary sitting devoted to oral questions. Before the sitting, the House of Representatives publishes the schedul of the sitting (pdf file in arabic). The first page of this document (the schedule) contains the following  data (see picture below) :

   + Time allocated to parliamentary groups
   + Ministries invited to the sitting
 
   ***Illustration***
  
![F2tables](https://user-images.githubusercontent.com/49843367/173394096-8c4a5c67-4f91-47c4-9bc2-72c1f0cca76b.png)

To get the schedule use the function : `getSchedule(path)` where `path` is the document path
```python
path= ".../ordre_du_jour_30052022-maj_0.pdf"
schedual = getSchedule(path)
```
The output `schedual` is  a dictionary  with the following keys :
   + "President": The president of the session
   + "nbrQuestTotalSession" : Total nbr of questions
   + "Ministries" : 
         
                    - "nomsMinister" : Name of ministers present in the session
                    - "numsQuest" : Total Number of question per minister
                    - "numQuestU": Number of urgent (أنى)  question
   + "Groups":
      
              + "nomsGroup" : Parliament groups
              + "quesTime": Time allocated for each group
              + "addTime" : Time for additional comments



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

To get the raw transcripts  use the function : `getRawTrscp(path,start=1,end=-1,two_side=True)` where `path` is the document path, `start` is the number of the page from where you want to begin extracting text (The first page is 1 not 0!) , `end` is number of the page where you want to stop extracting text and `two_side`if the pdf has two sides one in the left and the other in the right.
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
getRawTrscp

To store the output of `getRawTrscp`  in a folder use :`texToDir(path_pdf,parent_dir,start=1,end=-1,two_side=True,both_format=True,file_type='json')` where:
    
  - `path_pdf` : pdf path
  - `parent_dir` : directory where to create the folder where to store data
  - `start (default=1)` : Number of the page from where you want to begin extracting text.The first page is 1 not 0!
  - `end (default=-1)` : Number of the page to where you want to stop extracting text
  - `both_format (default=True)` :True if you want to store file in json AND txt format.If it's False, you may sepecify format with `file_type`
  - `file_type (default ='json')` : json or txt. It `both_format= True`, you don't need to use this parameter

This function creates a new folder having the same name of the pdf file (purple box, see image below) in the parent directory (red box). Depending on arguments, we can find three type of files in the new created folder : a JSON file containing the complete  text of the transcipt (all of it),  text files each one containes text of a specific page and a text file with the complete text.

***Example***
```python
path_pdf='C:/Users/pc/Desktop/ParlWatch/42-cdr23052022WF.pdf'
parent_dir='C:/Users/pc/Desktop/ParlWatch/'
texToDir(path_pdf,parent_dir,start=1,end=4,both_format=True)
```


![directory](https://user-images.githubusercontent.com/49843367/173596919-fad89543-5df4-49bb-9cff-26f759f7552c.png)


### IV. Deputy data and parliamentary activities
Each deputy has a section at the parliament website where we can find the following data :
  
  + General info about the deputy : Name, Party, Group, District ...
  + Parliamentary tasks: 
  + Deputy Agenda: 
  + Deputy Questions: Total number of questions and for each question we can find the folliwing details :
  
                           + Question date
                           + Question id
                           + Question title
                           + Question status : if the question received a response or not
                           + Date Answer
                           + Question text 

To get this data use the function :`getDeputy(url,include_quest=True,quest_link=False,quest_det=False)` where 
  + `url` : link to the deputy link 
  + `include_quest` (default=True): True to retuen data about deputy questions
  + `quest_link` (default=False) : True to include links of each question
  + `quest_det`(default=False): True to include question details (question text, Date Answer ...)

There is two ways to get the `url`of a deputy : `getUrls()` and `getUrlByName(name)`. The first one outputs a dictionary of the complete list of deputies and there urls. The last one outputs the url of the deputy `name`. 

```python
url_bouanou=getUrlByName("Abdellah Bouanou") ## Get the link of Abdellah Bouanou
url_bouanou  # 'https://www.chambredesrepresentants.ma/fr/m/abouanou'
```


```python
url="https://www.chambredesrepresentants.ma/fr/m/adfouf"
# We can have three scenarios
first=getDeputy(url)
second=getDeputy(url,include_quest=True)
tird=getDeputy(url,quest_link=True,quest_det=True)
```
The output is a dictionary with the structure below :

          {"Nom":name,"description":desc, "task":task,"Agenda":agenda,"Questions":Quests}
In first scenario we get :
```python
{'Nom': {'Député': ' Abdelmajid El Fassi Fihri'},
 'description': {'Parti': "Parti de l'istiqlal",
  'Groupe': "Groupe Istiqlalien de l'unité et de l'égalitarisme",
  'Circonscription': 'Circonscription locale',
  'Circonscription_1': 'Fès-Chamalia',
  'Legislature': '2021-2026',
  'Membre des sections parlementaires': ' Commission Parlementaire Mixte Maroc-UE                                                                                            '},
 'task': {'Commission': "Commission de l'enseignement, de la culture et de la communication"},
 'Agenda': {'Agenda_1': {'heure': '15:00',
   'evenemnt': 'Séance plénière mensuelle des questions de politique générale lundi 13 Juin 2022'},
  'Agenda_2': {'heure': '10:00',
   'evenemnt': 'Séance plénière mardi 7 Juin 2022 consacrée à la discussion du rapport de la Cour des Comptes 2019-2020'},
  'Agenda_3': {'heure': '15:00',
   'evenemnt': 'Séance plénière hebdomadaire des questions orales lundi 6 Juin 2022'},...}},
 'Questions': {'NbrQuest': ['12'],
  'Dates': ['Date : 20/04/2022',
   'Date : 04/03/2022',..],
  'Questions': ['Question  :  ترميم المعلمة التاريخية دار القايد العربي بمدينة المنزل، إقليم صفرو',
   'Question  :  المصير الدراسي لطلبة أوكرانيا'..],
  'Status': ['R', 'NR', ..],
  'Quest_link': [],
  'Quest_txt': []}}
```

In the third scenario,'Quest_txt' is different than [] and we get:
```python
'Quest_txt': [{'Nombre Question': ' 3475',
    'Objet ': ' ترميم المعلمة التاريخية دار القايد العربي بمدينة المنزل، إقليم صفرو',
    'Date réponse ': ' Mercredi 8 Juin 2022',
    'Date de la question': 'Mercredi 20 Avril 2022',
    'Question': 'صدر مرسوم رقم 2.21.416 ( 16 يونيو 2021) بالجريدة الرسمية عدد 7003 بإدراج المعلمة التاريخية "دار القايد العربي" بمدينة المنزل بإقليم صفرو في عداد الآثار، حيث أصبحت خاضعة للقانون رقم 22.80 المتعلق بالمحافظة على المباني التاريخية والمناظر والكتابات المنقوشة والتحف  الفنية والعاديات، وأكد صاحب الجلالة الملك محمد السادس في الرسالة السامية التي وجهها إلى المشاركين في الدورة 23 للجنة التراث العالمي في 27 مارس، 2013 ، "أن المحافظة على التراث المحلي والوطني وصيانته إنما هما محافظة على إرث إنساني يلتقي عنده باعتراف متبادل جميع أبناء البشرية".وقد طالبت جمعية التضامن للتنمية والشراكة بمدينة المنزل بإقليم صفرو، دون الحصول على رد، بتخصيص ميزانية لترميم هذه الدار التاريخية وتحويلها إلى مؤسسة ثقافية لخدمة ساكنة المنطقة وشبابها بخلق دينامية ثقافية لتكون منارة للأجيال القادمة.وعليه، نسائلكم السيد الوزير المحترم، ماهي الاجراءات التي ستتخذها وزارتكم قصد ترميم وتأهيل معلمة دار القايد العربي بمدينة المنزل بإقليم صفرو وتحويلها إلى مؤسسة ثقافية في إطار عدالة مجالية.'},...]
```

## Question ? 
Contact me on Twitter [@AmineAndam](https://twitter.com/AmineAndam)  or on Linkedin [ANDAM AMINE](https://www.linkedin.com/in/amineandam/).



                       

    
                    




