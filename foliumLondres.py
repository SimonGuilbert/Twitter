# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 09:34:17 2020

@author: simon
"""
# =============================================================================
# Carte OpenStreetMap
# =============================================================================
import folium

#Coordonnées GPS du centre de Londres
coordCentreLondres = [51.5055612,-0.1173717]

# Création de la carte avec le thème "stamentoner"
m = folium.Map(location=coordCentreLondres,
               tiles='stamentoner',
               zoom_start=6)

# Message qui s'affiche quand on met la souris sur la localisation d'un tweet
tooltip = "Cliquez pour voir le tweet"

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
# Requête pour récupérer les tweets stockés dans la table tweetsLondres de la BBD (rechTweetsLondres.py)
# =============================================================================
requete = "SELECT latitude,longitude,tweet FROM tweetsLondres"
cursor.execute(requete)

# La méthode 'fetchall ()' récupère les lignes de la dernière instruction exécutée (= requete)
result = cursor.fetchall() 

# Récupération du nombre total de tweets traités
cursor.execute("SELECT COUNT(*) FROM tweetsLondres")
nombreTotal = cursor.fetchall()
nombreTotal = str(nombreTotal[0])[1:][:4]

# =============================================================================
# Recherche des 10 mots les plus utilisés dans les tweets postés à Londres le 22/02/2020
# =============================================================================

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

# Renvoie une liste des mots les plus utilisés (= les mots dont leur fréquence d'apparition
# est identique et maximale dans le dictionnaire pris en paramètre). 
# Un mot est ignoré s'il appartient à la liste stopwords
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

# Fonction qui utilise les fonctions créées précédemment et affiche les 10 mots ayant la plus grande fréquence d'apparition        
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
    print("Sur un total de",nombreTotal,"tweets comptabilisés")

# Liste contenant des mots qui sont souvent utilisés pour donner du sens à une phrase, mais qui ne sont pas des 
# mots importants. Ca peut être des déterminants (the,a,an,...), un pronom (himself,herself,...), un sujet(I,you,he,she,...) 
# ou encore un auxiliaire (do,can,...)
stopwords = []
f = open("stopwords.txt", "r")
for mot in f:
    stopwords.append(mot[:-1])

# On ajoute à la liste des stopwords des chaînes de caractère qui reviennent souvent mais qui ne sont pas vraiment des mots
stopwords.append("&amp;")
stopwords.append("-")
stopwords.append("@" )
stopwords.append("m")

# =============================================================================
# Affichage du résultat
# =============================================================================
affichageResultat()

# Sauvegarde de la carte
m.save('carteLondres.html')

