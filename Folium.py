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
# Classe
# =============================================================================
class Carte:
    """classe gerant la carte avec folium"""
    def __init__(self,coord=[48.8534,2.3488]):
        """
        Parameters
        ----------
        coord :TYPE: Liste , optional.
            DESCRIPTION:contient les coordonnees de depart. The default is [48.8534,2.3488] qui correspond à Paris.
        Returns
        -------
        None.
        """
        self.carte=fl.Map(location=coord)
        
    def cercle(self,coord,rayon,color='crimson'):
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
        color='crimson',
        fill=True,
        fill_color=color).add_to(self.carte)
    def marqueur(self,coordonnee,popupstr,tooltip):
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
        fl.Marker(coordonnee, popup='<i>'+str(popupstr)+'</i>', tooltip=tooltip,icon=fl.Icon(color='black',icon_color='yellow',icon='glyphicon-user')).add_to(self.carte)
    def save(self,fil='index.html'):
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
        self.carte.save("html\\"+fil)
        
    def polygon(self,locations, tooltip=None,popup=True):
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
        fl.Polygon(locations,popup,tooltip).add_to(self.carte)
        
    def departement(self):
        """
        Ajoute les departements sur la carte.
        Returns
        -------
        None.
        """
        with open('G:\IDU\IDU s6\ISOC\TP\data\departement.json','r') as json_file:
            data=json.load(json_file)            
        for index in range(len(data['features'])):
            coord=self.inverse_coordonnee(data['features'][index]['geometry']['coordinates'][0])
            self.polygon(coord,data['features'][index]['properties']['code'],data['features'][index]['properties']['nom']) 
        
    def inverse_coordonnee(self,coord):
        """
        Inverse les coordonnees longitudinale et altitude
        Parameters
        ----------
        coord : TYPE: Liste
            DESCRIPTION:  contient la liste des differents coordonnees

        Returns
        -------
        coord_final : TYPE: Liste
            DESCRIPTION: liste des coordonnées inversées
        """
        coord_final=[]
        for index in range(len(coord)):
            coord_final.append([coord[index][1],coord[index][0]])
        return coord_final
    def requete_coord(self,ville,pays,url="https://nominatim.openstreetmap.org/search.php?q="):
        """
        recuperation des coordonnees GPS d'une ville

        Parameters
        ----------
        ville : TYPE:String
            DESCRIPTION: Nom de la ville
        pays : TYPE : String 
            DESCRIPTION : Nom du pays 
        url : TYPE: String, optional
            DESCRIPTION: contient l'url de l'api openStreetMap The default is "https://nominatim.openstreetmap.org/search.php?q=".

        Returns
        -------
        TYPE: Json
            DESCRIPTION:Json de la requete 

        """
        requete=(requests.get(url+ville+"+"+pays+'&polygon_geojson=1&format=json')).json()
        return requete
        if requete[0]["geojson"]["type"]=="Polygon":
            return requete[0]["geojson"]["coordinates"]
        else:
            return requete[0]["geojson"]["coordinates"]
    def requete_ville(self,altitude,longitude,url="https://nominatim.openstreetmap.org/reverse?lat="):
        """
        Parameters
        ----------
        altitude : TYPE:float
            DESCRIPTION: Contient 
        longitude : TYPE: float
            DESCRIPTION:
        url : TYPE, optional
            DESCRIPTION. The default is "https://nominatim.openstreetmap.org/reverse?lat=".

        Returns
        -------
        requete : TYPE
            DESCRIPTION.

        """
        requete=(requests.get(url+str(altitude)+"&lon"+str(longitude)+'&polygon_geojson=1&format=json')).json()
        return requete

        
        
        
        
        