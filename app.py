import os

from flask import Flask, render_template, request
from config import REDDIT_CLIENT_ID, REDDIT_API_KEY, SENDGRID_API_KEY, RECEIVING_EMAIL, TEMPLATE_ID

import atexit
import praw
import re
import sendgrid
from apscheduler.schedulers.background import BackgroundScheduler
from sendgrid.helpers.mail import *

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():


    # send email per day
    # https://stackoverflow.com/questions/21214270/scheduling-a-function-to-run-every-hour-on-flask
    # https://stackoverflow.com/questions/16932825/why-cant-non-default-arguments-follow-default-arguments

    # List of timezone
    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Los_Angeles'})
    scheduler.start()
    scheduler.add_job(send_meme,'cron', hour=6, minute=0, end_date='2022-05-30')


    atexit.register(lambda: scheduler.shutdown())

    return "hi"

# this function deal with the api
def send_meme():


    # getting today's newest meme from reddit
    
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                  client_secret=REDDIT_API_KEY,
                  user_agent='USERAGENT',
                  username='MemeDose')

    memesub = reddit.subreddit('meme')

    new = memesub.new(limit = 50)

    
    today_meme = []

    for meme in new:
        if not meme.stickied and is_image(meme.url) and len(today_meme) < 10:
            today_meme.append(meme.url)
            

    # Send it to email using sendgrid

    # https://sendgrid.com/docs/for-developers/sending-email/v3-python-code-example/
    # https://sendgrid.com/docs/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates/

    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": RECEIVING_EMAIL,
            }
          ],
          "dynamic_template_data":{

              "image_link0" : today_meme[0],
              "image_link1" : today_meme[1],
              "image_link2" : today_meme[2],
              "image_link3" : today_meme[3],
              "image_link4" : today_meme[4],
              "image_link5" : today_meme[5],
              "image_link6" : today_meme[6],
              "image_link7" : today_meme[7],
              "image_link8" : today_meme[8],
              "image_link9" : today_meme[9]              
          }
        }
      ],
      "from": {
        "email": "memeeveryday@gmail.com"
        
      },
      "content": [
        {
          "type": "text/plain",
          "value": "Meme Delivered"
        }
      ],
      "template_id": TEMPLATE_ID
    }

    try:
        
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=data)
        print("Email was sent")
        return True
    except:
        print("Error: Email was not sent")
        return False

    return False



def is_image(meme_url):

    return re.search(r'jpg$', meme_url) or (re.search(r'png$', meme_url))

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
