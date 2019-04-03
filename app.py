import os

from flask import Flask, render_template, request
from config import REDDIT_CLIENT_ID, REDDIT_API_KEY, SENDGRID_API_KEY, RECEIVING_EMAIL, TEMPLATE_ID

import atexit
import flask
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
    scheduler.add_job(func=keep_awake, trigger="interval", minutes=10)
    scheduler.add_job(send_meme_gmail,'cron', hour=6, end_date='2022-05-30')
    

    atexit.register(lambda: scheduler.shutdown())
    

    return render_template('index.html')

@app.route("/display_meme", methods=['GET', 'POST'])
def display_meme():
    
    meme_sub = flask.request.args.get('meme_sub')
    sortby = flask.request.args.get('sortby')
    quantity = flask.request.args.get('quantity')

    memelist = get_meme(meme_sub, sortby, quantity)

    return flask.jsonify({'memelist':memelist})


# empty function to prevent heroku dyno from sleeping
def keep_awake():
    print("function to keep app awake")
    return None



# getting today's newest meme from reddit, return as a list of image links
def get_meme(meme_sub, sortby, quantity):
      
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                  client_secret=REDDIT_API_KEY,
                  user_agent='USERAGENT',
                  username='MemeDose')

    memesub = reddit.subreddit(meme_sub)


    try:
        quantity = int(quantity)
        if (quantity > 20):
            quantity = 20
        elif (quantity <= 0):
            quantity = 5
    except:
        quantity = 5
    

    meme_page = None
    if (sortby == "new"):
        meme_page = memesub.new(limit = quantity*2)
    elif (sortby == "hot"):
        meme_page = memesub.hot(limit = quantity*2)
    elif (sortby == "rising"):
          meme_page = memesub.rising(limit = quantity*2)

    
    meme_list = []

    for meme in meme_page:
        if not meme.stickied and is_image(meme.url):
            meme_list.append(meme.url)
        if (len(meme_list) >= quantity):
            break            

    return meme_list


# this function send to my email with the sendgrid api
def send_meme_gmail():

    today_meme = get_meme()
            
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
        print("Gmail was sent")
        return True
    except:
        print("Error: Gmail was not sent")
        return False

    return False



def is_image(meme_url):

    return re.search(r'jpg$', meme_url) or re.search(r'png$', meme_url)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
