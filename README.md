# Timesheet reminder
python code to send email to remind to submit timesheet

- send email with html content
- send email at every 28th of each month
- use python anywhere as hosting

## Idea
 - To use a while loop to keep the program running
 - program will send an email if the date is 28th of each month ( as every month will have a 28 day)
 - program will send the email at 12.05am.
 - it will connect to the free gmail smtp server to send the email via ssl
 - After sending it will sleep till next day.
 
 ### Installation

send_reminder.py requires [python 3](https://www.python.org/) to run.

Install the dependencies and devDependencies and start the python code.

```sh
$ pip install -r requirements.txt
$ python send_reminder.py
```
 
 ## Technology used.
 | Name | Description |
| ------ | ------ |
| Python Anywhere | For hosting : https://www.pythonanywhere.com/ |
| Datetime | For datetime manipulation |
| smtplib | To send email |
 
 
