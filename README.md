
# Project Title

Water level measurment and alert system

# Description
This is a rest API based project using python which measures water level and automaticaly sends an alert message if a threshold is crossed from randomly chosen stations along riven Elbe. Firstly, three random stations are selected and the corresponding datas from API are reuested. Then a dataframe is created from the json file which contains only the required informations namely the current time, location and the watel level. The data is collected in a CSV file in an interval of five minutes. Then the collected water level data are checked with a defined thresold value which triggers an automated alert email. You can give your email in the variable alert_recipitent and change the thresold to check the functionality of the code.       
## Installation
Language- Python3;
library- requests, pandas;
SMTP module: yagmail.
For easy installation of all the required modules and libraries you can install the requirement.txt file in your terminal before running the code.
    
## API Reference

#### Get all items

```http
  https://pegelonline.wsv.de/webservice/guideRestapi
```
