# open decision
<br>
We are building an Open-Source Decision Automation System, that is optimized for legal processes. The system will be used to build a platform for legal advice for consumers in Germany.
<br> Further information on <a href="open-decision.org">open-decision.org</a>

## Architecture
The system is split in several different applications.
<br> The **builder** app enables legal scholars to build complex decision trees without requiring technical knowledge. The builder is currently developed using the Python web-framework Django. The decision trees can be exported to plain JSON, the logic is currently encoded using JsonLogic.
<br> The decision trees can be interpreted on several plattforms.
<br> Website: The website is currently developed using Django for back- and front-end, soon it will use React as front-end.
<br> Apps: Using React Native, apps for Android and iOS are planned.
<br> Chat-Bot: A demo of the [Telegram-Bot](https://github.com/fbennets/Legal-Decision-Automation-telegram) is already running, Facebook and WhatsApp bots are planned.

### Setup
