# -*- coding: utf-8 -*-
"""
S'éxécute après la génération du réseau de portes 

objectif du script :
    - définir les fonctions pour modéliser le processus de markov
    - simuler l'évolution du réseau de portes étudié
    
En entrée :
    -Conditions initiales (vecteur X à t=0, contient la taille de la population)
    -Pas de temps delta_t, date initiale t0, date de fin t_final
"""

import datetime

import numpy as np

import pandas as pd

import pickle

###### Conditions initiales et paramétrage

N_personne = 100

delta_t = datetime.timedelta(seconds=10)

t0 = datetime.datetime(year=2019,month=1,day=1,second=0,minute=0)

t_final =  datetime.datetime(year=2019,month=1,day=8,second=0,minute=0)

data = pd.DataFrame(columns=["id_piece_depart","id_piece_arrivee","id_porte","sens_porte","date"])


##### fonction mise à jour de l'état du sytème

# la fonction doit permettre de générer l'état suivant un état donné
# comme la transition entre les états du système entraîne le passage de portes,
# cette fonction réalise la création du jeu de données

def maj_markov(X_actuel,P,t,matrice_adj,liste_porte):

   X_nouveau=[0]*len(X_actuel)
   
   indice_piece = [i for i  in range(len(X_actuel))]
   
   for i in range(len(X_actuel)):
       
       # vecteur de probabilité de transition depuis la piece i
       proba = P[i]
       # nombre de personne actuellement dans le piece i
       N_personne = X_actuel[i]
       # liste du nombre de personne se déplaçant de la piece i aux autres pieces
       deplacement = np.random.choice(indice_piece,N_personne,p=proba)
       
       # pour chaque personne initialement dans la piece i, on reporte
       # le déplacement dans la matrice X_nouveau, et dans le cas d'un changement
       # le passage de portes dans la variable data
       for j in deplacement :
           
           X_nouveau[j]+=1
           
           # on ajoute aux données quand des portes sont empruntées
           if j != i :
               
               # le cas où il y a une seule porte qui va de i à j
               if matrice_adj[i][j] == 1 : 
                   
                   indice_porte = liste_porte.index([i,j])
                   
                   data.loc[len(data)] = [i,j,indice_porte,1,t]
                   
               elif matrice_adj[j][i] == 1 :
                   
                   indice_porte = liste_porte.index([j,i])
                   
                   data.loc[len(data)] = [i,j,indice_porte,-1,t]
                  
               # dans le cas où plusieurs portes existent, on tire au hasard la porte
               # qui sera empruntée, puis on crée la donnée associée à cette porte
               elif matrice_adj[i][j] > 1 :
                   
                   porte_possible = [indice for indice,x in enumerate(liste_porte) if x==[i,j] ]
                   
                   data.loc[len(data)] = [i,j,np.random.choice(porte_possible),1,t]
                   
               elif matrice_adj[j][i] > 1 :

                   porte_possible = [indice for indice,x in enumerate(liste_porte) if x==[j,i] ]
                   
                   data.loc[len(data)] = [i,j,np.random.choice(porte_possible),1,t]
   
   return(X_nouveau)

##### Fonction pour générer une matrice de transition aléatoire

# une situation est représentée par une matrice d'adjacence une liste des portes
# à partir de cette représentation, on veut pouvoir générer un matrice
   
# comme expliqué dans le rapport, la matrice de transition dépend du moment de la 
# journée cette différence sera traduite par la liste "coeff_comportement" qui indique le poids des
# différents cas d'utilisation 
def creer_matrice_transition(matrice_adj,coeff_comportement):
    
    matrice = np.array([[0]*N_piece]*N_piece)
    
    # coefficient pour les personnes qui restent à l'extérieur du réseau
        
    for i in range(N_piece_ext):
        
        matrice[i][i] += coeff_comportement[0]
    
    
    # coefficient pour les personnes qui restent dans une pièce du réseau
    
    for i in range(N_piece_ext,N_piece):
        
        matrice[i][i] += coeff_comportement[1]
        
    # coefficient pour les personnes d'emprunter une porte dans le sens direct
    # traduit l'avancée en profondeur dans le réseau
    
    matrice += coeff_comportement[2] * matrice_adj
    
    # coefficient pour les personnes d'emprunter une porte dans le sens indirect
    # traduit l'avancée vers la sortie du réseau
    
    matrice += coeff_comportement[3] * np.transpose(matrice_adj)
     
    
    # en dernière étape de la fonction, on normalisera les lignes de cette matrice
    # afin que la somme des coefficients sur une même ligne fasse 1
    # (condition pour une matrice de transition)
    
    matrice = matrice.astype(float)
    
    for i in range(len(matrice)):
    
        # le cas total[i]=0 ne survient pas car les coefficients sont positifs strict
        matrice[i] = 1/(sum(matrice[i])) * matrice[i]
    
    return(matrice) 
    

        
##### Script pour générer des données
    
# initialisation
    
X_actuel = [0]*N_piece

t=t0

liste_comportement = [[1,60,40,5],[1,100,30,5],[100,5,1,100],[1000,1,1,100],[100000,1,1,1]]

#[1,60,40,5] le matin (8-10h)
#[1,100,30,5] la journée (10-16h)
#[100,5,1,100] le soir (16-20h)
#[1000,1,1,100] la nuit (20-8h)
#[100000,1,1,1] le weekend


liste_matrice_transition=[]

for comportement in liste_comportement:
    
    liste_matrice_transition.append(creer_matrice_transition(matrice_adj, comportement))

# répartition homogène des personnes au niveau des pièces extérieures à t0

for i in range(N_piece_ext):
    
    X_actuel[i]= N_personne // N_piece_ext

# s'il reste des personnes à attribuer, on les attribue aléatoirement sur les autres pieces
reste = N_personne%N_piece_ext

while reste > 0 :
     
    X_actuel[np.random.randint(0,N_piece_ext-1)] += 1
    
    reste = reste -1
    
# génération des données 
    
while t <= t_final :
    
    print(t)
    
    if t.weekday()>4:
        
        matrice_transition = liste_matrice_transition[4]
        
    else :
        
        if t.hour >=8 and t.hour <10:
            
            matrice_transition = liste_matrice_transition[0]
            
        if t.hour >=10 and t.hour <16:
            
            matrice_transition = liste_matrice_transition[1]

        if t.hour >=16 and t.hour <20:
            
            matrice_transition = liste_matrice_transition[2]

        if t.hour >=20 or t.hour <8:
            
            matrice_transition = liste_matrice_transition[3]
        
    
    X_actuel=maj_markov(X_actuel, matrice_transition, t, matrice_adj, liste_porte)
    
    t = t + delta_t

def save_data():
    
    file = open('data_pickle', 'wb')
    
    pickle.dump(data,file)
    
    file.close()
    
    
    file = open('liste_porte','wb')
    
    pickle.dump(liste_porte,file)
    
    file.close()
    
    
    file = open('matrice_adjacence','wb')
    
    pickle.dump(matrice_adj,file)
    
