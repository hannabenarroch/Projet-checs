import matplotlib.pyplot as plt
import pandas as pd
from chess_functions import *


#on cherche le joueur qui a joué le plus de match
def actif(con):
    max = 0
    actif = 0
    for player in con.execute("select id from player"):
    
        longueur = len(list(con.execute("select tournoi from match where white_player = ? or black_player =?", (player[0],player[0],))))
        if longueur>max :
            max = longueur
            actif = player[0]
    nom_joueur = list(con.execute("select name from player where id = ?", (actif,)))[0][0]
    print(nom_joueur, actif)
    print(max)
    return nom_joueur


#Les défaites et victoires selon la couleur
def victoire_couleur(joueur, con):
    #taper_votre_joueur = "tieres cristiano"
    taper_votre_joueur = joueur

    hist = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]
    print(id_joueur)

    hist['victoire_blanc']=0
    for row in con.execute("select tournoi from match where white_player = ? and winner =1", (id_joueur,)):
        hist['victoire_blanc']+=1

    
    hist['victoire_noir']=0
    for row in con.execute("select tournoi from match where black_player = ? and winner =0", (id_joueur,)):
        hist['victoire_noir']+=1

    
    hist['defaite_blanc']=0
    for row in con.execute("select tournoi from match where white_player = ? and winner =0", (id_joueur,)):
        hist['defaite_blanc']+=1

    
    hist['defaite_noir']=0
    for row in con.execute("select tournoi from match where white_player = ? and winner =1", (id_joueur,)):
        hist['defaite_noir']+=1

    #print(hist)

    df = pd.DataFrame.from_dict(hist, orient='index')
    df.plot(kind='bar')


# +
#L'évolution du elo

def elo_evolution(con, joueur):
    taper_votre_joueur = joueur

    tournoi = []
    elo = []

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]

    for row in list(con.execute("select tournoi,elo_black from match where black_player =?", (id_joueur,))):
        if not row[0] in tournoi:
            tournoi.append(row[0])
            elo.append(int(row[1][:-1]))
    for row in list(con.execute("select tournoi,elo_white from match where white_player =?", (id_joueur,))):
        if not row[0] in tournoi:
            tournoi.append(row[0])
            elo.append(int(row[1][:-1]))

    plt.plot(tournoi, elo)

#remarque : il faudrait tracer ça en fonction du temps car sinon ça ne veut rien dire 


# +
#Top 10 des adversaires rencontrés

def top_adversaires(con, joueur):
    taper_votre_joueur = joueur

    adversaires = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]
    print(id_joueur)

    for row in con.execute("select name from player join match on player.id = match.black_player where match.white_player = ?", (id_joueur, )):
        adversaire = row[0]
        if adversaire not in adversaires.keys():
            adversaires[adversaire]=1
        else :
            adversaires[adversaire]+=1
        
    for row in con.execute("select name from player join match on player.id = match.white_player where match.black_player = ?", (id_joueur, )):
        adversaire = row[0]
        if adversaire not in adversaires.keys():
            adversaires[adversaire]=1
        else :
            adversaires[adversaire]+=1
        
    df = pd.DataFrame.from_dict(adversaires, orient='index')
    df.plot(kind='bar')


# +
#Nombre de matchs par mois sur une période

def number_match(con, joueur):
    taper_votre_joueur = joueur

    matchs = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]
    print(id_joueur)

    for row in con.execute("select distinct date from tournois join match on tournois.id = match.tournoi where match.white_player = ? or match.black_player =?", (id_joueur, id_joueur,)):
        mois =  date_debut(row[0])[2]
        annee = date_debut(row[0])[3]
        if mois+annee not in matchs.keys():
            matchs[mois+annee]=1
        else :
            matchs[mois+annee]+=1

    df = pd.DataFrame.from_dict(matchs, orient='index')
    df.plot(kind='bar')
# -


