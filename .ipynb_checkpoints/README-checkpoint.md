# Projet-checs

Le site de référence est echecs.asso.fr

__But du projet :__

Il s’agirait de matcher chaque joueur dans une base de données, avec l’ensemble des matchs dans lesquels il a joué ayant été répertoriés sur le site, récupérer aussi la liste des joueurs contre qui il a joué avec les résultats, et éventuellement des statistiques. 

Pour cela il faut faire une boucle sur les tournois qui ont été joués dans tout le site, en collectant les données des résultats.

Le rendu de ce projet serait sur Python.

La deuxième partie serait de la reconnaissance d'écriture sur les fiches de tournois, avec détection d'erreur (partie plus difficile).


# Démarche

<!-- #region -->
Les tournois sont tous affiliés à un Id sur le site. Pour parcourir tous les tournois, on fait donc une boucle sur les numéros des Id.

Il y a deux types de grilles en échec : les grilles américaines (http://www.echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/53714/53714&Action=Ga), et les grilles berger (http://www.echecs.asso.fr/Resultats.aspxURL=Tournois/Id/55214/55214&Action=Berger).
Nous avons créé des fonctions permettant de lire et récupérer les informations de la page html pour les deux types de tournoi.





Nous nous sommes ensuite demandés comment stocker toutes les informations collectées sur le site. 
Nous voulions d'abord les organiser sous la forme d'un grand dictionnaire Python, puis sous la forme d'un fichier csv, mais les données que nous avions à stocker (joueurs, noms des tournois, dates des tournois, rencontres entre joueurs, couleurs jouées, gagnant de chaque rencontre, elos) étaient trop complexes. 


Nous avons finalement opté pour une base de donnée SQL avec 3 tables : la table player, la table tournois, et la table match. 

La table player contient les colonnes : id (int), name (str)

La table tournois contient les colonnes : id (int), name (str), date (str), rondes(int), cadence (str), type (berger ou américain)(str)

La table match contient les colonnes : id (int), tournoi (int), black_player (int), elo_black (str), white_player (int), elo_white (int), winner (int)


Note :  l'id de la table tournoi correspond exactement à l'id du site, ce qui facilite l'update.

Note : pour la colonne winner de match : 
- 0 pour victoire des noirs
- 3 pour victoire des noirs si l'adversaire n'est pas venu
- 1 pour victoire des  blancs
- 4 pour victoire des blancs si l'adversaire n'est pas venu, 
- 2 pour ex aequo




Nous avons ensuite réglé les problèmes liés à la lecture des très anciens matchs, car il n'y avait pas encore de standardisation de la présentation des grilles. 


Nous avons fait tourner la base de données, et avons ensuite créé des fonctions incluant des requêtes SQL pour afficher des statistiques sur un joueur donné.


Nous avons ensuite essayé de créer une page html pouvant faire office d'interface client, afin de mieux présenter les données et graphes que nous avions réussi à créer jusque là.
<!-- #endregion -->

# Document utilisateur 

<!-- #region -->
Le fichier *chess_functions.py* regroupe toutes les fonctions nécessaire à l'extraction d'informations des pages du site. S'y trouvent aussi les fonctions test sur les dates des tournois, et la fonction *database* permettant de remplir la base de données.

Le fichier *stats.py* regroupe toutes les fonctions permettant de récupérer des informations, de réaliser des graphiques et des statistiques sur un joueur en envoyant des requêtes à la base de données. 

La démarche est la suivante. 
Il faut d'abord remplir la base de données avec tous les tournois qui ont été joué jusqu'à présent. On se rend sur le fichier *data_build.py*, on crée le fichier au format .db, et on lance la fonction database, qui fait une boucle sur les numéros des tournois sur le site. Le premier tournoi répertorié a un id 18324, et le dernier est vers les 55 000. Pour s'assurer de tous les parcourir, et comme ils ne sont pas exactement classés par ordre chronologique, on met une borne finale de 60 000. On enregistre bien la base de données créée.


Ensuite on va dans le fichier *main.py*. On se connecte au fichier de la base de données, qu'on commence par updater à aujourd'hui. Puis on peut faire des tests sur un joueur dont on tape le nom + prénom tout en minuscule. Dans le fichier actuellement les tests ont été faits avec "herve daurelle" qui a participé à beaucoup de tournois sur plusieurs années. On peut ainsi connaître des informations sur l'évolution de la participation, des elos, et des victoires du joueur. 
<!-- #endregion -->

```python

```
