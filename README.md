# DoorNetwork
Door network simulation, getting coherent network with parametrability

Simulation de réseau de porte, obtention paramétrable de réseau de porte cohérent


Les scripts présents dans le dossier sont à éxécuter l'un après l'autre
dans l'ordre suivant :

1) script_generer_probleme:

Ce script génère un réseau de portes avec les paramètres précisés
dans la partie "paramétrage"

Nécessite les libraires :
-random
-graphviz
-numpy

2) script_generer_data : 

Ce script simule le déplacement du nombre d'une population dans le réseau
de porte généré par le script 1). Les comportements sont précisés dans la
partie "génération des données".

Le paramétrage inclut :
-le nombre de personnes N_personne (type = int)
-le pas de temps delta_t (type = timedelta)
-le temps initial t0 et final t_final (type = datetime)

Nécessite les libraires :
-datetime
-numpy
-pandas
-pickle

3) script_analyse_data : 

Ce script réalise le calcul des métriques et les tracés graphiques
précisés dans le rapport, sur les données précédemment générées.
Les métriques sont accessibles en tant que variable et les graphiques sont
sauvegardées dans la working directory.
Le script est plutôt long, certains print on été placés pour suivre les calculs.


Nécessite les libraires :
-datetime
-numpy
-pandas
-pickle
-matplotlib

