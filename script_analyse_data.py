# -*- coding: utf-8 -*-
"""
Objectif du script :
    - calculer différentes métriques sur le jeu de données généré
    - créer des graphiques représentatifs des comportements
"""

import datetime

import numpy as np

import pandas as pd

import pickle

import matplotlib.pyplot as plt

# fonction pour charger les variables python de données si besoin
def load_data():
    
    file = open('data_pickle', 'rb')
    
    data = pickle.load(file)
    
    file.close()
    
    
    file = open('liste_porte','rb')
    
    liste_porte = pickle.load(file)
    
    file.close()

##### étude du nombre d'utilisation de chaque porte (dans les 2 sens)

print('etude du nombre d'utilisation')

# nombre d'utilisation dans les deux sens

compteur1=[]

for i in range(len(liste_porte)):
    
    compteur1.append(len(data.loc[data['id_porte']==i]))
    
# nombre d'utilisation dans le sens direct
    
compteur2 = []

data2 = data.loc[data['sens_porte']==1]

for i in range(len(liste_porte)):
    
    compteur2.append(len(data2.loc[data2['id_porte']==i]))
    
# nombre d'utilisation dans le sens indirect
    
compteur3 = []

data3 = data.loc[data['sens_porte']==-1]

for i in range(len(liste_porte)):
    
    compteur3.append(len(data3.loc[data3['id_porte']==i]))
    
# portes les plus utilisées quelque soit le sens
    
metrique1 = [indice for indice,x in enumerate(compteur1) if x == max(compteur1)]

# portes les plus utilisées dans le sens direct

metrique2 = [indice for indice,x in enumerate(compteur2) if x == max(compteur2)]

# portes les plus utilisées dans le sens indirect
    
metrique3 = [indice for indice,x in enumerate(compteur3) if x == max(compteur3)]

##### étude de l'activité sur le réseau de porte dans le temps
# on met la donnée du sens d'ouverture des porte sous forme de série temporelle

print('etude de l'activite')

liste_date = []

t=t0

while t <= t_final:
    
    liste_date.append(t)
    
    t = t+delta_t


liste_1,liste_2,liste_3 = [0]*len(liste_date),[0]*len(liste_date),[0]*len(liste_date)


for i in range(len(data)) :
    
    print(i)
    
    date = data['date'][i]
    
    indice_date = liste_date.index(date)
    
    if data['sens_porte'][i] == 1 :
        
        liste_1[indice_date] += 1
    
        liste_2[indice_date] += 1

    else :
        
        liste_1[indice_date] += 1

        liste_3[indice_date] += 1 

#dates auxquelles on a le plus de passage de porte peu importe le sens
        
metrique4 = [liste_date[indice] for indice,x in enumerate(liste_1) if x == max(liste_1)]


#dates auxquelles on a le plus de passage dans le sens direct

metrique5 = [liste_date[indice] for indice,x in enumerate(liste_2) if x == max(liste_2)]

#dates auxquelles on a le plus de passage dans le sens indirect

metrique6 = [liste_date[indice] for indice,x in enumerate(liste_3) if x == max(liste_3)]

# dates auxquelles il y a eu le moins de passage

metrique7 = [liste_date[indice] for indice,x in enumerate(liste_1) if x ==min(liste_1)]

# dates auxquelles il y a eu le moins de passage dans le sens direct

metrique8 = [liste_date[indice] for indice,x in enumerate(liste_2) if x ==min(liste_2)]

# dates auxquelles il y a eu le moins de passage dans le sens indirect

metrique9 = [liste_date[indice] for indice,x in enumerate(liste_3) if x ==min(liste_3)]



# tracé graphique de l'activité sur l'ensemble de la période étudiée
# sauvegardé dans le fichier "graphique_activite.png"

plt.plot(liste_date,liste_1,'r--',label='trafic cumulé')

plt.plot(liste_date,liste_2,'b--', label='trafic entrant')

plt.plot(liste_date,liste_3,'g--',label='trafic sortant')

plt.legend()

fig = plt.gcf()

fig.set_size_inches(60, 20)

fig.savefig('graphique_activite.png',dpi=200)

######évolution de l'effectif présent dans la zone réglementé (càd, pas dans des pièces extérieures)

print('etude de l'evolution de l'effectif au sein du reseau')

# avant le déplacement à t0, l'effectif dans le réseau est nul

effectif = [0]

# on parcourt les données à chaque date, et on fait évoluer l'effectif si des portes
# vers ou depuis extérieures sont empruntées
for i in range(len(liste_date)):
    
    print(i)
    
    effectif_actuel = effectif[-1]
    
    data4 = data[data['date'] == liste_date[i]]
    
    for elem in data4['id_piece_depart']:
        
        if elem < N_piece_ext:
            
            effectif_actuel+=1
            
    for elem in data4['id_piece_arrivee']:
        
        if elem < N_piece_ext:

            effectif_actuel-=1
        
    effectif.append(effectif_actuel)
    
# tracé graphique de l'évolution de l'effectif dans le réseau

effectif.pop(0)

plt.plot(liste_date,effectif,'r--',label='nombre de personnes dans le réseau')

plt.legend()

fig = plt.gcf()

fig.set_size_inches(60, 20)

fig.savefig('graphique_effectif.png',dpi=200)
