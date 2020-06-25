# -*- coding: utf-8 -*-
"""
fonction : création d'un réseau de porte aléatoire, suivant les paramètre donnés


paramètres :
    -N_piece : nombre de pieces
    -N_porte : nombre de portes
    -N_piece_ext : nombre de pieces qui correspondent au points d'accès du réseau depuis l'extérieur
    
"""

import random 

from graphviz import Digraph

import numpy as np


###### Paramétrage pour générer le réseau de portes

N_porte = 200

N_piece = 120

N_piece_ext = 30

# on génère la liste des pieces

liste_piece = []

for i in range(N_piece_ext):
    
    liste_piece.append('piece_ext_'+str(i))

for i in range(N_piece-N_piece_ext):
    
    liste_piece.append('piece_int_'+str(i))
    
    
##### fonction de génération de la matrice d'adjacence

def creer_matrice_adj():
    
    matrice = np.array([[0]*N_piece]*N_piece)
   
    # pour l'ensemble des pieces, on crée au moins une porte
    # cette porte est forcément dans le sens entrant si la piece i est extérieure  
    for i in range(N_piece):
               
        # si la piece i est extérieure, on lui ajoute une porte vers l'intérieur
        # donc le coefficient se place en ligne i sur la matrice d'adjacence
        # la piece vers laquelle la porte mene doit être intérieure
        if i < N_piece_ext :
            
            j = random.randint(N_piece_ext,N_piece-1)
            
            matrice[i][j] += 1
        
        # si la piece i est intérieure, on peut lui ajouter une porte vers
        # une piece j intérieure (dans ce cas, le sens direct ou indirect)
        # ou extérieure (dans ce cas, le sens est indirect)
        if i >= N_piece_ext :
            
            j = random.randint(0,N_piece-1)
            
            # on vérifie qu'on a deux pieces différentes pour créer une porte
            while j==i:
                j = random.randint(0,N_piece-1)
            
            
            # on tire un entier dans {0,1}, pour déterminer le sens de la porte
            # quand les deux pièces sont intérieures
            tirage = random.randint(0,1)
            
            # si la piece j est exterieure, on ajoute une porte dans le sens indirect
            if j < N_piece_ext or tirage==0:
                matrice[j][i]+=1
            
            if j >= N_piece_ext and tirage==1:
                matrice[i][j]+=1
    # création de portes supplémentaires jusqu'à obtenir le nombre de portes désiré
    
    while sum(sum(matrice)) < N_porte :
        
        i = random.randint(0,N_piece-1)
        
        if i < N_piece_ext :
            
            j = random.randint(5,N_piece-1)
            
            matrice[i][j]+=1
            
        if i >= N_piece_ext :
            
            j = random.randint(0,N_piece-1)
            
            while j == i :
                
                j = random.randint(0,N_piece-1)
            
            tirage = random.randint(0,1)
            # si la piece j est exterieure, on ajoute une porte dans le sens indirect
            
            if j < N_piece_ext or tirage==0:
                
                matrice[j][i]+=1
            
            if j >= N_piece_ext and tirage==1:
                
                matrice[i][j]+=1 
                
    # La correction de la matrice d'adjacence obtenue pour vérifier qu'il n'y a pas :
    # 1-de contradiction dans le sens des portes
    # 2-qu'il y ait toujours un chemin de sortie (càd qui mène à une pièce extérieure)
    
    # on regarde la partie triangulaire inférieure, pour les coeffs de la matrice non nuls,
    # on regarde le coeff symétrique, si celui ci est non nul, on somme les deux, on les 
    # remplace par 0 et on place la somme dans la ligne adaptée (si une pièce est extérieure 
    # ce sera impérativement et uniquement la piece i)
    for i in range(1,N_piece):
        
        for j in range(1,i):
            
            if matrice[i][j] != 0 and matrice[j][i] != 0:
                
                a = matrice[i][j] + matrice [j][i]
                
                matrice[i][j] = 0
                matrice[j][i] = 0
                
                matrice[i][j] = a
    
    # pour vérifier qu'il y ait toujours un chemin de sortie, il suffit de vérifier que
    # toutes les pièces intérieures possèdent une porte qui permettente d'y entrer.
    # par récursivité, celà veut dire que toutes les pièces possèdent un chemin de sortie.
    # En pratique, on vérifie que pour toutes les pieces i > N_piece_ext, on peut trouver un
    # entier j qui vérifier matrice[j][i] != 0
    # si ce n'est pas le cas, on peut ajouter un lien entre cette piece i et un piece 
    # extérieure choisie au hasard
    for i in range(N_piece_ext+1,N_piece):
        
        k = 0
        
        for j in range(N_piece):
            
            if matrice[j][i] != 0 :
                
                k = 1
                
                break
            
        if k == 0 :
            
            matrice[random.randint(0,N_piece_ext-1)][i]+=1
                                
    return(matrice)

##### Création du réseau de portes
    
matrice_adj = creer_matrice_adj()

# une porte est composé d'un id, d'un numéro de pièce entrant et sortant

liste_porte = []

g = Digraph('G', filename='graphe_probleme')

for piece in liste_piece :
    
    g.node(piece)
    
    indice_porte = 0 #pour numéroter les portes

for i in range(N_piece):
    
    for j in range(N_piece):
        
        if matrice_adj[i][j]>0:

            n = matrice_adj[i][j]#dans le cas où il y a plusieurs portes
            
            while n>0:
                
                g.edge(liste_piece[i], liste_piece[j],label = 'porte_'+str(indice_porte))
            
                liste_porte.append([i,j])
            
                indice_porte+=1
                
                n = n-1
    
#affichage de la modélisation du problème  : g.view()

                
