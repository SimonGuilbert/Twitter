# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:12:39 2020

@author: simon
"""

import folium
from math import sqrt,pi,radians, cos, sin, asin

#Coordonnées GPS de Polytech Annecy
centre = [45.9196872,6.1581842]

# Création de la carte avec le thème "stamentoner"
m = folium.Map(location=centre,
               tiles='stamentoner',
               zoom_start=2)

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

# Requête permettant de récupérer uniquement les tweets contenant des coordonnées GPS
requete = "SELECT latitude,longitude,tweet FROM treizeMilleTweets WHERE latitude <> 99.999 or longitude <> 99.999"

## executing the statement using 'execute()' method
cursor.execute(requete)

## 'fetchall()' method fetches all the rows from the last executed statement
result = cursor.fetchall() 

for line in result:
    folium.Marker([line[0], line[1]], 
              popup='<i>'+str(line[2])+'</i>', 
              tooltip=tooltip,
              icon=folium.Icon(color = "black",
                               icon_color = "orange",
                               icon = "glyphicon-user")
              ).add_to(m)
    
#folium.Rectangle([-0.46582,51.32216,0.20091,51.64730]).add_to(m)
m.save('carteMonde.html')





