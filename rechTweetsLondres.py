# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:02:57 2020

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
# =============================================================================try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '•••••••••'
ACCESS_SECRET = '•••••••••'
CONSUMER_KEY = '•••••••••'
CONSUMER_SECRET = '•••••••••'

# Authentification
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# =============================================================================
# Recherche des tweets postés à Londres (avec la méthode du Streaming API)
# =============================================================================
'''
    → Pour chaque tweet posté à Londres
        • On insère les informations suivantes du tweet dans la base de données
            ♣ id (identifiant attribué pour chaque tweet)
            ♣ text (texte du tweet)
            ♣ coordinates["coordinates"][0] = longitude
            ♣ coordinates["coordinates"][1] = latitude
            ♣ user.location (adresse de l'auteur du tweet)
'''
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
        
# Recherche des tweets postés à Londres
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(locations=[-0.5239,51.2206,0.2871,51.7405])

