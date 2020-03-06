# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:10:59 2020

@author: Jonathan Molieres
"""

# =============================================================================
# import
# =============================================================================
import mysql.connector as mysql
# =============================================================================
# Classe
# =============================================================================
class Mysql:
    """classe gerant la connection avec la base sql et la modifiant si necessaire"""
    def __init__(self,a_user,password,a_host="localhost"):
        """
         Parameters
        ----------
        user : TYPE:String 
            DESCRIPTION:nom d'utilisateur pour ce connecter à la base
        password : TYPE:String
            DESCRIPTION: mot de passe pour ce connecter à la base
        host : TYPE:String, optional
            DESCRIPTION: The default is "localhost".

        Returns
        -------
        None.

        """
        self.base = mysql.connect(
            host = a_host,
            user = a_user,
            passwd = password,
            use_pure=True)
        
    def execute(self,requete):
        """
        Parameters
        ----------
        requete : TYPE: String 
            DESCRIPTION: contient la requete en sql

        Returns
        -------
        None.

        """
        cursor = self.base.cursor()
        cursor.execute(requete)
        
    def recuperation_donnee(self,requete):
        cursor = self.base.cursor()
        cursor.execute(requete)
        myresult = cursor.fetchall()
        return myresult
    
    def ajout_base(self,requete,values):
        """
        Parameters
        ----------
        requete : TYPE:String
            DESCRIPTION : requete sql
        values : TYPE:Tuple
            DESCRIPTION: valeur à ajouter à la base

        Returns
        -------
        None.
        """
        cursor = self.base.cursor()
        cursor.execute(requete, values)
        self.base.commit()
        
    def montrer_base(self,nom_table):
        """
        Parameters
        ----------
        nom_base : TYPE:String
            DESCRIPTION: contient le nom de la table à visualiser

        Returns
        -------
        None.
        """
        requete="SELECT * FROM "+str(nom_table)
        cursor = self.base.cursor()
        cursor.execute(requete)
        records = cursor.fetchall()
        for record in records:
            print(record)
            
    def close(self):
        """ deconnection du serveur """
        self.base.close()