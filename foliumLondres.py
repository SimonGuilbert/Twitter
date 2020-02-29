# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 09:34:17 2020

@author: simon
"""

import folium
from math import sqrt,pi,radians, cos, sin, asin

#Coordonnées GPS du centre de Londres
coordCentreLondres = [51.5055612,-0.1173717]

# Création de la carte avec le thème "stamentoner"
m = folium.Map(location=coordCentreLondres,
               tiles='stamentoner',
               zoom_start=6)

tooltip = "Cliquez pour voir le tweet"

# =============================================================================
# Connecting to the database
# =============================================================================
# importing 'mysql.connector' as mysql for convenient
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

# Requête permettant de récupérer les tweets postés à Londres
requete = "SELECT latitude,longitude,tweet FROM tweetsLondres"

## executing the statement using 'execute()' method
cursor.execute(requete)

## 'fetchall()' method fetches all the rows from the last executed statement
result = cursor.fetchall() 

# Renvoie un dictionnaire ayant pour clés les mots des tweets et pour valeur leur fréquence d'apparition
# La fonction ajoute aussi les marqueurs de position (grâce aux coordonnées GPS des tweets) sur la carte "m"
def frequenceMots(data):
    mots = {}
    for ligne in data:
        folium.Marker([ligne[0], ligne[1]], 
              popup='<i>'+str(ligne[2])+'</i>', 
              tooltip=tooltip,
              icon=folium.Icon(color = "black",
                               icon_color = "orange",
                               icon = "glyphicon-user")
              ).add_to(m)
        for mot in ligne[2].replace(","," ").replace("'"," ").split(" "):
            if mot in mots:
                mots[mot] += 1
            else:
                mots[mot] = 1
    return mots

# Fonction qui renvoie la première clé d'un dictionnaire
def premiereCle(dic):
    for cle in dic.keys():
        return cle

# Renvoie une liste des mots les plus utilisés 
# (= les mots dont leur fréquence d'apparition est identique et maximale dans le dictionnaire)   
def meilleursMots(dic):
    res = []
    meilleurMot = premiereCle(dic)
    for mot in dic.keys():
        if dic[mot] > dic[meilleurMot] and mot.lower() not in stopwords:
            res = [[mot,dic[mot]]]
            meilleurMot = mot
        elif dic[mot] == dic[meilleurMot] and mot.lower() not in stopwords:
            res.append([mot])
    return res
        
def affichageResultat():
    print("  _____                 _ _        _ \n |  __ \               | | |      | |\n | |__) |___  ___ _   _| | |_ __ _| |_\n"+
         " |  _  // _ \/ __| | | | | __/ _` | __|\n | | \ \  __/\__ \ |_| | | || (_| | |_\n |_|  \_\___||___/\__,_|_|\__\__,_|\__|")
    print("\nLes 10 mots les plus utilisés dans les tweets postés à Londres le 22 février 2020 entre 10h et 18h (UTC+1) sont : ")
    freq = frequenceMots(result)
    compt = 0
    while compt < 10:
        for mot in meilleursMots(freq):
            print(" ♦",mot[0])
            stopwords.append(mot[0].lower())
            compt += 1

#    print("Avec une fréquence d'apparition de",liste[0][1],"parmi",len(result),"tweets")

stopwords = []
f = open("stopwords.txt", "r")
for mot in f:
    stopwords.append(mot[:-1])
stopwords.append("&amp;")
stopwords.append("-")
stopwords.append("@" )
stopwords.append("m")

# Utilisation des fonctions pour afficher le résultat
affichageResultat()
   
m.save('carteLondres.html')