# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:42:14 2020

@author: Jonathan Molieres
"""
# =============================================================================
# import
# =============================================================================
import folium as fl
import json
import requests


# =============================================================================
# Class
# =============================================================================
class Carte:
    """classe gerant la carte avec folium"""

    def __init__(self, coord=None):
        """
        Parameters
        ----------
        coord :TYPE: Liste , optional.
            DESCRIPTION:contient les coordonnees de depart. The default is [48.8534,2.3488] qui correspond à Paris.
        Returns
        -------
        None.
        """
        if coord is None:
            coord = [45.89912, 6.12871]
        self.carte = fl.Map(location=coord,zoom_start=6)

    def cercle(self, coord, rayon, color='crimson'):
        """
        Permet d'ajouter un cercle à la carte
        Parameters
        ----------
        coord : TYPE: Liste de floattant
            DESCRIPTION: Liste des coordonnees
        rayon : TYPE: entier
            DESCRIPTION: determine le rayon du cercle
        color : TYPE:String , optional
            DESCRIPTION: Definie la couleur du cercle,The default is 'crimson'.

        Returns
        -------
        None.
        """
        fl.Circle(
            radius=rayon,
            location=coord,
            popup='The Waterfront',
            color=color,
            fill=True,
            fill_color=color).add_to(self.carte)

    def marqueur(self, coordonnee, popupstr, tooltip):
        """
        Place un marqueur sur la carte
        Parameters
        ----------
        coordonnee : TYPE:Liste
            DESCRIPTION: Liste des coordonnees 
        tooltip : TYPE: String 
            DESCRIPTION:String visible
        popupstr : TYPE: String
            DESCRIPTION: String visible lorsqu'on clique sur le marqueur

        Returns
        -------
        None.
        lien pour modifier l'apparence des icones : getbootstrap.com/docs/3.3/components/
        """
        fl.Marker(coordonnee, popup='<i>' + str(popupstr) + '</i>', tooltip=tooltip,
                  icon=fl.Icon(color='black', icon_color='orange', icon='glyphicon-cutlery')).add_to(self.carte)

    def save(self, fil='index.html'):
        """
        Fonction de creaction du html
        Parameters
        ----------
        fil : TYPE: String, optional
            DESCRIPTION: titre du fichier The default is 'index.html'.

        Returns
        -------
        None.
        """
        self.carte.save("html\\" + fil)

    def polygon(self, locations, tooltip=None, popup=True):
        """
        Trace un polygon sur la carte.
        Parameters
        ----------
        locations : TYPE: Liste  des coordonnees
            DESCRIPTION:
        tooltip : TYPE: String visible sur la carte, optional
            DESCRIPTION: phrase à ajouter.The default is None.
        popup : TYPE: String visible lorsqu'on clique sur le polygon,optional
            DESCRIPTION. The default is True.
        Returns
        -------
        None.
        """
        fl.Polygon(locations, popup, tooltip).add_to(self.carte)
