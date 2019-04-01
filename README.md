# Legal-Decision-Automation 
<br>
We are building an Open-Source Decision Automation System, that is optimized for legal processes. The project is a collaboration of several Law Clinics and Legal Tech initiatives throughout Germany. Currently the developement is coordinated by the Consumer Law Clinic of the Humboldt-University Berlin. The system will be used to build a platform for legal advice for consumers in Germany.

## Architecture
The system is split in several different applications. 
<br> The **builder** app enables legal scholars to build complex decision trees without requiring technical knowledge. The builder is currently build using the Python web-framework Django. The decision trees can be exported to plain JSON, the logic is currently encoded using Jsonlogic.
<br> The decision trees can be interpreted on several plattforms. 
<br> Website: The website is currently build using Django for back- and front-end, soon it will use React as front-end.
<br> Apps: Using React Native, apps for Android and iOS are planned.
<br> Chat-Bot: A demo of the [Telegram-Bot](https://github.com/fbennets/Legal-Decision-Automation-telegram) is already running, Facebook and WhatsApp bots are planned.

**The code is still quite messy, cleaning will take place the next weeks**
