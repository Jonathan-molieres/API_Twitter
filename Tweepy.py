# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:36:03 2020

@author: molierej
"""
# =============================================================================
# import
# =============================================================================
import tweepy
import json
from baseSQL import Mysql


# =============================================================================
# Connection à la base sql
# =============================================================================
base=Mysql("root","Jona1998than")#completer avec nom et mdp
base.execute("USE basetwitter")#choix de la base
base.execute("CREATE TABLE IF NOT EXISTS tweets (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, place VARCHAR(255),coordonne_x float(11),coordonne_y float(11) ,description VARCHAR(255))")#creaction de base 
# =============================================================================
# Fonction
# =============================================================================
def moyenne(coordonnee):
    """
    Parameters
    ----------
    coordonnee : TYPE: liste
        DESCRIPTION: Liste de coordonnees

    Returns
    -------
    list
        DESCRIPTION: retourne la moyenne des coordonnees

    """
    moyenne_x=0
    moyenne_y=0
    n=len(coordonnee)
    for i in range(n):
        moyenne_x+=coordonnee[i][0]
        moyenne_y+=coordonnee[i][1]
    return [moyenne_y/n,moyenne_x/n]
# =============================================================================
# class pour le streaming de l'API twitter
# =============================================================================
class StreamListener(tweepy.StreamListener):
    """class permetant la lecture de l'api de tweeter"""
    def on_status(self, status):
        self.type_donnee='sql'
        #permet de choisir le choix de l'enregistrement de la donnee
        #entre json et sql dans le dernier cas, il faut avoir installer SQL
        if self.type_donnee=='json':
            if status._json['place']:
                print(status._json['place'])
                print(status._json['place']['bounding_box'])
                with open('data\data.json','r') as json_file:
                    data=json.load(json_file)
                datas={'status':status._json['place']['bounding_box'],'text':status._json['text'],'place':status._json['place']}
                data.append(datas)
                with open('data\data.json','w') as json_file:
                    json.dump(data,json_file,indent=3)
        elif self.type_donnee=='sql':
        
            if status._json['place']:
                print(status._json['text'])
                coord=moyenne(status._json['place']['bounding_box']['coordinates'][0])
                base.ajout_base("INSERT INTO tweets (place,coordonne_x,coordonne_y,description) VALUES (%s,%s,%s,%s)",(status._json['place']["name"],coord[0],coord[1],status._json['text']))
    def setType(self,type_donnee):
        """
        Parameters
        ----------
        type_donnee : TYPE:String
            DESCRIPTION:Choix du type de format pour la base de tweets

        Returns
        -------
        None.

        """
        self.type_donnee=type_donnee
        
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
