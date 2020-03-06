# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:12:34 2020

@author: Jonathan Molieres
"""
class Analyse:
    """classe permetant l'analyse des tweets"""
    def __init__(self):
        self.mot_inutile=[]# Liste des Stop word
        self.mot={}#dictionnaire des mots frequents avec leur compteur
        #recuperation des mots inutiles
        with open('G:\IDU\IDU s6\ISOC\TP\data//STOPWORD.txt','r') as txt_file:
            for ligne in txt_file:
                self.mot_inutile.append(ligne[:-1])#suppresion des sauts de 
    def get_mot(self):
        """
        Returns
        -------
        TYPE:dictionnaire
            DESCRIPTION: dictionnaire des mots frequents avec leur compteur

        """
        return self.mot
    
    
    def trouver_mot_inutile(self,mot_rechercher):
        """
        Parameters
        ----------
        mot_rechercher : TYPE: String 
            DESCRIPTION: mot a verifier dans la liste

        Returns
        -------
        bool
            DESCRIPTION: Vrai si le mot rechercher fait partie des stop words
                         Faux sinon.
        """
        for mots in self.mot_inutile:
            if mots==mot_rechercher or mots[0].upper()+mots[1:]==mot_rechercher:
                return True
        return False 
               
    def ajout_tweet(self,data):
        """
        Ajoute au dictionnaire les mot valide

        Parameters
        ----------
        data : TYPE: String
            DESCRIPTION: texte du tweet

        Returns
        -------
        None.

        """
        ponctuation=[' ',',',"'","  ",";","!","...","?","",':','-',"’","«","»"]#Liste des ponctuations
        tweet=data.lower().split()#liste de chaque mot sans majuscule
        
        for mot_entier in tweet:
            # permet de decouper les mots avec des apostrophes
            if len(mot_entier.split("’")) >len(mot_entier.split("'")):
                mot_sans_apostrophe=mot_entier.split("’") 
            else:
                mot_sans_apostrophe=mot_entier.split("'") 
                
            for mot in mot_sans_apostrophe:
                if not self.trouver_mot_inutile(mot) and not mot=='':
                    if not  mot[0]=='@' and not mot[:4]=="http" and not mot in ponctuation and not  mot[0]=='#':
                        
                        if mot in self.mot.keys():#verification si le mot est dans le dictionnaire
                                self.mot[mot] = self.mot[mot]+1
                        else:
                            self.mot[mot] = 1
    def maximum(self):
        """
        Recherche du compteur maximum dans le dictionnaire
        Returns
        -------
        key_max : TYPE: String
            DESCRIPTION: clé avec le compteur maximum
        """
        compteur=0
        key_max=''
        for key in self.mot.keys():
            if compteur==0:
                key_max=key#premier clé pour initialise la fonction
                compteur+=1
            if self.mot[key]>self.mot[key_max]:
                key_max=key
        return key_max
                    
    def frequence_total(self,nombre):
        """
        Parameters
        ----------
        nombre : TYPE: int
            DESCRIPTION: nombre de mot frequent qu'on souhaite afficher

        Returns
        -------
        resultat : TYPE: Dictionary
            DESCRIPTION: mot frequent avec les compteurs associes

        """
        resultat={}
        for i in range(nombre):
            key_max=self.maximum()
            self.__str__(key_max,self.mot[key_max])#fonction d'affichage
            resultat[key_max]=self.mot[key_max]
            del self.mot[key_max]        
        return resultat
            
            
            
    def __str__(self,mot,compteur):
        '''
        fonction d'affichage
        Parameters
        ----------
        mot : TYPE: chaine de caractere
            DESCRIPTION: mot qui apparait souvent
        compteur : TYPE: entier 
            DESCRIPTION: nombre de fois qu'apparait le mot

        Returns
        -------
        None.
        '''
        print("Le mot '"+str(mot)+"' apparait "+str(compteur)+" fois sur l'échantillons de tweets.")
             
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            