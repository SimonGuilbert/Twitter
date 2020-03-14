# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:12:39 2020

@author: simon
"""
# =============================================================================
# Carte OpenStreetMap
# =============================================================================
import folium

#Coordonnées GPS de Polytech Annecy
centre = [45.9196872,6.1581842]

# Création de la carte avec le thème "stamentoner" centré en Polytech
m = folium.Map(location=centre,
               tiles='stamentoner',
               zoom_start=2)

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
# Requête pour sélectionner les tweets dont on connaît l'information sur la localisation
# =============================================================================

# Requête permettant de récupérer uniquement les tweets contenant des coordonnées GPS
requete = "SELECT latitude,longitude,tweet FROM treizeMilleTweets WHERE latitude <> 99.999 or longitude <> 99.999"
cursor.execute(requete)

# La méthode 'fetchall ()' récupère les lignes de la dernière instruction exécutée (= requete)
result = cursor.fetchall() 

# =============================================================================
# Ajout des points sur la carte
# =============================================================================

# Message qui s'affiche quand on met la souris sur la localisation d'un tweet
tooltip = "Cliquez pour voir le tweet"

'''
    → Pour chaque ligne du résultat de la requête
        • On ajoute un marqueur à la carte à l'emplacement :
            ♣ line[0]=longitude
            ♣ line[1]=latitude
        • Si on clique sur le marqueur, on affiche line[2]=texte du tweets
        • Si on passe la souris sur le marqueur, on affiche le tooltip
        • L'icône du marqueur est de la forme:
            ♣ Icône d'utilisateur
            ♣ De couleur orange
            ♣ Avec un fond noir
'''       
for line in result:
    folium.Marker([line[0], line[1]], 
              popup='<i>'+str(line[2])+'</i>', 
              tooltip=tooltip,
              icon=folium.Icon(color = "black",
                               icon_color = "orange",
                               icon = "glyphicon-user")
              ).add_to(m)

# Sauvegarde de la carte au format HTML 
m.save('carteMonde.html')





