# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:46:01 2020

@author: molierej
"""
# =============================================================================
# import
# =============================================================================
import tweepy
import json
from Folium import Carte
from Analyse import Analyse
from baseSQL import Mysql
from Tweepy import StreamListener
# =============================================================================
# fichier json 
# =============================================================================
fichier_donnee='data.json'
fichier_temp='temporaire.json'
# =============================================================================
# fonction 
# =============================================================================
def lecture(fichier):
    """
    Parameters
    ----------
    fichier : TYPE :chaine de caractere
        DESCRIPTION:nom du fichier à extraire

    Returns
    -------
    data : TYPE :
        DESCRIPTION :
    """
    with open('data//'+str(fichier),'r') as json_file:
        data=json.load(json_file)
    return data
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
    moyenne_x = 0
    moyenne_y=0
    n=len(coordonnee)
    for i in range(n):
        moyenne_x+=coordonnee[i][0]
        moyenne_y+=coordonnee[i][1]
    return [moyenne_y/n,moyenne_x/n]

def decomposition(data):
    """
    Parameters
    ----------
    data : TYPE:json
        DESCRIPTION: donnee recu par la lecture du json

    Returns
    -------
    coords : TYPE : Liste
        DESCRIPTION : Liste des coordonnees
    texts : TYPE: Chaine de caractere
        DESCRIPTION.
    L_moyenne : TYPE
        DESCRIPTION.
    """
    coords=[]
    texts=[]
    L_moyenne=[]
    for i in data:
        coordinates=[]
        L_moyenne.append(moyenne(i['status']['coordinates'][0]))
        for j in range(len(i['status']['coordinates'][0])):
            
            coordinates.append([i['status']['coordinates'][0][j][1],i['status']['coordinates'][0][j][0]])
        texts.append(i['text'])
        coords.append(coordinates)
    return coords,texts,L_moyenne

def recherche(data,ville):
    """
    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    ville : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    """
    with open('data//temporaire.json','r') as json_file:
        donnee=json.load(json_file)
        donnee=[]#supresion des donnees 
    for i in data:
        if i['place']['name']==ville:
            donnee.append(i)
    with open('data//temporaire.json','w') as json_file:
         json.dump(donnee,json_file,indent=3)
         
def sql(nom_base): 
    """
    recuperation des données par le serveur sql
    Returns
    -------
    L_moyenne : TYPE : Liste
        DESCRIPTION.
    texts : TYPE : Liste
        DESCRIPTION.
    place : TYPE : Liste 
        DESCRIPTION.

    """
    base=Mysql("root","Jona1998than") #completer avec nom et mdp
    base.execute("USE basetwitter") #choix de la base
    resultat=base.recuperation_donnee("SELECT * FROM "+str(nom_base))
    texts=[]
    L_moyenne=[]
    ville=[]
    
    if len(resultat[0])==5:
        for donnee in resultat:
            ville.append(donnee[1])
            L_moyenne.append([donnee[2],donnee[3]])
            texts.append(donnee[4])
            
        return L_moyenne,texts,ville 
    else:
        pays=[]
        for donnee in resultat:
            ville.append(donnee[1])
            pays.append(donnee[2])
            # L_moyenne.append([donnee[3],donnee[4]])
            texts.append(donnee[5])
            
        return ville,pays,texts
# =============================================================================
# Main
# =============================================================================
if __name__=='__main__':
    application=True
    print("=============================================================================")
    print("                           TP API TWITTER")
    print("=============================================================================")
    while application:
        
        print("Entrer ajouter pour rajouter des tweets a la base. Entrer analyse pour analyser les tweets."+
              "\nEntrer carte, pour afficher les tweets du monde avec l'analyse. Pour quitter, entrer exit.")
        fonction=input("Votre choix : ")
        if fonction == "analyse":

            type_donnee=input("Entrer le format des données entre sql et json : ")
            
            if type_donnee=='json':
                """Analyse des tweets de la base json et creaction de la carte des tweets"""
                fichier=lecture(fichier_donnee)#lecture du fichier de donnee
                resultat=decomposition(fichier)#decomposition des donnees
                carte=Carte()
                analyse=Analyse()
                for i in range(len(resultat[0])):
                    analyse.ajout_tweet(resultat[1][i])#analyse chaque tweets
                #analyse global et affichage
                analyse.__str__(analyse.frequence_total(10))
                for i in range(len(resultat[0])):
                    carte.marqueur(resultat[2][i],resultat[1][i],'')#ajout des marqueurs
                carte.save("json.html")#creation du html
                                
                print("=============================================================================")
                print("         Le html est crée dans le dossier html avec le nom json.")
                print("=============================================================================") 
                
            if type_donnee=='sql':
                """Analyse des tweets de la table tweets et creaction de la carte des tweets"""
                carte=Carte()
                resultat=sql("tweets")
                analyse=Analyse()
                for i in range(len(resultat[1])):
                    analyse.ajout_tweet(resultat[1][i])#analyse chaque tweet
                #analyse global et affichage
                analyse.__str__(analyse.frequence_total(10))
                for i in range(len(resultat[0])):
                    carte.marqueur([resultat[0][i][0],resultat[0][i][1]],resultat[1][i],resultat[2][i])#ajout des marqueurs
                carte.save("sql.html")#creation du html
                print("=============================================================================")
                print("         Le html est crée dans le dossier html avec le nom sql.")
                print("=============================================================================")
                
        elif fonction == "carte":
            """Analyse des tweets par ville de la table tweets_france et creaction de la carte des tweets"""
            carte=Carte()
            resultat=sql("tweets_france")
            compteur_ville={}
            for i in range(len(resultat[0])):
                if (resultat[0][i],resultat[1][i]) in compteur_ville.keys():
                    compteur_ville[(resultat[0][i],resultat[1][i])]+=(1,[resultat[2][i]]+compteur_ville[(resultat[0][i],resultat[1][i])][1])
                else:
                    compteur_ville[(resultat[0][i],resultat[1][i])]=(1,resultat[2])
            analyse=Analyse()
            for key in compteur_ville.keys():
                """verifier la requete et gerer en sql"""
                analyse.renitilaiser_mot()
                for txt in compteur_ville[key][1]:
                    analyse.ajout_tweet(txt)
                # print(carte.requete_coord(key[0],key[1])
                try:
                    requete=carte.requete_coord(key[0],key[1])                
                    if requete[0]["geojson"]["type"]=="Polygon":
                        carte.polygon(carte.inverse_coordonnee(requete[0]["geojson"]["coordinates"][0]),compteur_ville[key][0],analyse.phrase_resultat(analyse.frequence_total(3)))
                    elif requete[0]["geojson"]["type"]=="Point":
                        carte.marqueur(carte.inverse_coordonnee(requete[0]["geojson"]["coordinates"]),analyse.phrase_resultat(analyse.frequence_total(3)),compteur_ville[key][0])
                except:
                    pass
            carte.save("carte.html")
            print("=============================================================================")
            print("         Le html est crée dans le dossier html avec le nom carte.")
            print("=============================================================================") 
        elif fonction == "ajouter":
            """Permet d'ajouter des nouveaux tweets aux bases"""
            # Variables that contains the user credentials to access Twitter API 
            ACCESS_TOKEN = '1222959339163594752-NOAONLptGZvumYp2gTNSElFjixkP8i'
            ACCESS_SECRET = 'QkH6pFC7nO69Ctk6plc2DJGWry6njuVq59TL7PzduTIrM'
            CONSUMER_KEY = '54ElR6xtokKeFt8fygBdgNhhZ'
            CONSUMER_SECRET = 'QGLBx1H3AlquacgEa08yO8MXujrMi3rHOb1n6hejctQgbxq8CK'
            # Connection
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True)
            
            type_donnee=input("choix du type de donnee entre sql et json : ")
            myStreamListener = StreamListener()
            myStreamListener.setType(type_donnee)
            if type_donnee=="sql":
                nom_base=input("Choix de la base(tweets,tweets_france,tweets_paris) : ")
                myStreamListener.set_nom_base(nom_base)
            print("Pour quitter, veuillez quitter la console.")
            # Lancement de la recuperation de donnee sur l'API de streaming 
            myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
            myStream.filter(locations=[2.177757,48.754530,2.519654,48.951081])
            myStream.filter(country=["fr"])
        elif fonction == "exit":
            """Permet de quitter"""
            application=False
        
        
        
        
        
        
        
        
        