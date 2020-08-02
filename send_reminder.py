import email.message
import smtplib
import time
import logging
from calendar import monthrange
from datetime import datetime, timedelta
from pytz import timezone
import os
import json


# gmail settings
with open("config.json") as json_data_file:
    settings_file = json.load(json_data_file)
gmail_user = settings_file['gmail_user']
gmail_password = settings_file['gmail_pwd']
msg = email.message.Message()


# logging settings
logging.basicConfig(filename='reminder.log', level=logging.DEBUG)

# helper functions
def reload_daily_settings():
    """
    To reload the settings that are changed daily
    """
    # get current date, 28th of each month and last day of month
    # get last day of month code from https://stackoverflow.com/questions/42965501/get-last-day-of-month-in-python
    current = datetime.now(tz=timezone('Asia/Singapore'))
    current_date = current.date().strftime('%d-%m-%Y')
    the_28th_date = current.replace(day=28).date().strftime('%d-%m-%Y')
    endmonth = monthrange(current.year, current.month)
    lastdayofmonth = datetime(current.year, current.month, endmonth[1])
    lastdayofmonth = lastdayofmonth.strftime('%d-%m-%Y')
    # email content
    sent_from = gmail_user
    to = settings_file['recipients']
    subject = '[Reminder] Submit Leave Form at BGC Portal'
    body = """Hi Guys ,
    <br>
    <h2> Please be reminded to : <br> <u style="color: #AF5B5B;"> Submit your Leave Form</u> <br>
    at BGC portal by : <br> <u style="color: #AF5B5B;" > The end of the month - (%s)</u> .</h2>
    <br>
    <hr>
    <p>You will be reminded at every 28 of the month.</p>
    <p>Thanks for subscribing to the Auto reminder system</p> <hr>
    <br>
    <br>
    - %s""" % (lastdayofmonth, sent_from)
    # msg settings
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ', '.join(to)
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)
    logging.info(current_date + ': settings set')
    return current_date , the_28th_date


def send_email():
    current = datetime.now(tz=timezone('Asia/Singapore'))
    current_date = current.date().strftime('%d-%m-%Y')
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()

        logging.info(current_date +': email sent')
    except Exception as e:
        logging.debug(current_date+ ' : '+ e)
        logging.debug(current_date + ': Something went wrong...')


def get_seconds_till_tmr():
    today = datetime.today()
    tomorrow = datetime.replace(
        today + timedelta(days=1), hour=0, minute=5, second=0)
    delta = tomorrow - datetime.now()
    return delta.seconds
#####################################################################################

# main function

def run_reminder():
    logging.info('starting program ...')
    while True:
        current_date, the_28th_date = reload_daily_settings()
        if current_date == the_28th_date:
            logging.info('sending email at : ' + current_date)
            send_email()
        seconds_till_tmr = get_seconds_till_tmr()
        logging.info('next check is at seconds later : ' + str(seconds_till_tmr))
        time.sleep(seconds_till_tmr)


if __name__ == "__main__":
    run_reminder()
