# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:02:57 2020

@author: guilbers
"""
## Connecting to the database

## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "vivelescours",
    use_pure=True
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

# Choix de la base de données
cursor.execute("USE twitter")

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '1225317572284907523-8fUF1DuvOvAAYg1BFW9Uvc04H0i5u1'
ACCESS_SECRET = 'MvsMQS7sH4QBw7KXdzbSZ4kXP9FRsXZj2Tu2e1f4GtlDJ'
CONSUMER_KEY = 'ggP7lKwr8ehEFQYgvZOcuhTrw'
CONSUMER_SECRET = 'w5hhK12LhkpBy3F5ZPvjkGkR1frF5fEfiMTX59xA4Ik4691bCn'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        query = "INSERT INTO tweetsLondres VALUES (%s,%s,%s,%s,%s)"
        if status.coordinates:
            values = (status.id, 
                      status.text,
                      status.coordinates["coordinates"][0],
                      status.coordinates["coordinates"][1],
                      status.user.location)
#           print(query,values)
            cursor.execute(query,values)
            db.commit()
             
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(locations=[-0.5239,51.2206,0.2871,51.7405])

