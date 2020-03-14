# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:38:32 2020

@author: guilbers
"""

# =============================================================================
# Connexion à la base de données
# =============================================================================
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "••••••••••••",
    use_pure=True
)

# Création d'une instance de la classe Cursor pour pouvoir exécuter du code SQL avec Python
cursor = db.cursor()

# Choix de la base de données
cursor.execute("USE twitter")

# =============================================================================
# Connexion à l'API
# =============================================================================
try:
    import json
except ImportError:
    import simplejson as json

import tweepy

# Identifiants de connexion à l'API Twitter
ACCESS_TOKEN = '1225317572284907523-8fUF1DuvOvAAYg1BFW9Uvc04H0i5u1'
ACCESS_SECRET = 'MvsMQS7sH4QBw7KXdzbSZ4kXP9FRsXZj2Tu2e1f4GtlDJ'
CONSUMER_KEY = 'ggP7lKwr8ehEFQYgvZOcuhTrw'
CONSUMER_SECRET = 'w5hhK12LhkpBy3F5ZPvjkGkR1frF5fEfiMTX59xA4Ik4691bCn'

# Authentification
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# =============================================================================
# Test du Search API
# =============================================================================
#tweet = tweepy.Cursor(api.search, q='Artificial Intelligence')

# =============================================================================
# Test du Streaming API
# =============================================================================
'''
    → Pour chaque tweet posté dans le monde contenant les mots clés "Artificial Intelligence" ou bien "IA"
        • Si l’information de localisation du tweet est présente (si status.place ≠ None)
            ♦ On insère les informations suivantes du tweet dans la base de données
                ♣ id (identifiant attribué pour chaque tweet)
                ♣ text (texte du tweet)
                ♣ place.bounding_box.coordinates[0][0][0] = longitude
                ♣ place.bounding_box.coordinates[0][0][1] = latitude
                ♣ user.location (adresse de l'auteur du tweet)
        • Sinon
            ♦ On insère les informations suivantes du tweet dans la base de données
                ♣ id
                ♣ text
                ♣ 99.999
                ♣ 99.999
                ♣ user.location
''' 

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        query = "INSERT INTO treizeMilleTweets VALUES (%s,%s,%s,%s,%s)"
        if status.place:
            values = (status.id, status.text,
                      status.place.bounding_box.coordinates[0][0][0],
                      status.place.bounding_box.coordinates[0][0][1],
                      status.user.location)
        else:
            values = (status.id, status.text,99.999,99.999,status.user.location)
        cursor.execute(query,values)
        db.commit()
             
    def on_error(self, status_code):
        if status_code == 420:
            return False

# On recherche les tweets contenant "Artificial Intelligence" ou bien "IA" écrits en anglais       
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["Artificial Intelligence","AI"],languages=["en"])

