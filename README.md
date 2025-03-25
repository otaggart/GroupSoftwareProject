# bestGroupProject
urls -   
http://127.0.0.1:8000    
http://127.0.0.1:8000/EnergyConservationMinigame  
http://127.0.0.1:8000/Recycle  
http://127.0.0.1:8000/bike_game  
http://127.0.0.1:8000/list  
http://127.0.0.1:8000/admin  
installations-  
pip install django
pip install qrcode  
pip install pillow 
pip install django-extensions
commands -  
python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver  

The group members are:  
  
Oscar Taggart  
Alex Saunders  
Regan Boateng  
Clarry Amofa  
Dylan Bradshaw  
Mirkazim Allahverdiyev  
Tin Lau  


This is a submission for Sprint 2. There are three types of document that you will find the following places.  

**PROCESS DOCUMENTS**
Our process documents are managed in the trello platform. The link to our project page is below. We (tinnoklau) have added solomonoyelere1 to the board so it is visible.  

trello link: [https://trello.com/b/Zdu9kVZD/kanban-board]  

We have also taken regular snapshots of the kanban board in trello to archive our progress. These are held in the repository below.  

https://docs.google.com/document/d/1V9aqwANRkeQJ3JtRS3k_rFP_eUM8QaQCVFfUZ8iU3Bc/edit?tab=t.0#heading=h.jm2pi5r4x4x8  

Within process documents we have also included the meeting notes, agenda and minutes. These will be found in the repository below.  

https://docs.google.com/document/d/1V9aqwANRkeQJ3JtRS3k_rFP_eUM8QaQCVFfUZ8iU3Bc/edit?tab=t.0#heading=h.jm2pi5r4x4x8  

**INSTRUCTIONS FOR USE**
to run the deployed version use the following link - https://bestgroupproject.onrender.com/

to host locally the above installs are required

Adminastrative and Game Management Uses:
admins should youse the /admin url to accesss the django administration page. From here they cand do a number of actions

quiz creation ~ to create a quiz minigame, first add a quiz. Once a quiz is added, questions must be added in the questions section and the quiz they are being added to must be selected in the drop down menu for each question. answers can be added from this menu or the answers menu and each question should have 1 correct answer. there is a results tabl that allows an adminto view the results of quizes in isolation from the main points system in order to gauge difficulty. The url /list is also a page accessible only to super users that allows any quiz to be accessed. this feature is primarily here so that the urls can be retrieved for the qr codes later.

qr code linking ~ admins can generate qr codes by enetering the website database section, to generate a qr code, click add then paste a url into the Name field and save. a file can be used to replace the generated qr code if needed.

Regular Users:
should access minigames via qr codes (can be found in our development documentation)
can navigate the rest of the website via the nav bar

**TECHNICAL DOCUMENTS**   
Our technical documents are primarily managed on the github system. The link to the project is below:  

github link: https://github.com/aSaunEXCS/bestGroupProject  
