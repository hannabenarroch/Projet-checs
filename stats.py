import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
        
        
    hist['nul_blanc']=0
    for row in con.execute("select tournoi from match where white_player = ? and winner =2", (id_joueur,)):
        hist['nul_blanc']+=1

    
    hist['nul_noir']=0
    for row in con.execute("select tournoi from match where white_player = ? and winner =2", (id_joueur,)):
        hist['nul_noir']+=1

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
            print(row[0], row[1])
            tournoi.append(row[0])
            elo.append(int(row[1][:-1]))
    for row in list(con.execute("select tournoi,elo_white from match where white_player =?", (id_joueur,))):
        if not row[0] in tournoi:
            print(row[0], row[1])
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
    
    #mettre que les adversaires qu'il a vus plusieurs fois 
    
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
        date =  datetime.strptime(str(date_debut(row[0])[1])+"-"+date_debut(row[0])[3], "%m-%Y")
        if date not in matchs.keys():
            matchs[date]=1
        else :
            matchs[date]+=1
    i=0
    data = dict()
    for key in matchs.keys():
        data[i]=[key, matchs[key]]
        i+=1

    df = pd.DataFrame.from_dict(data, orient='index', columns = ["date", "nombre"])
    df= df.sort_values(by='date') 

    plt.figure(figsize=(20, 10))
    ax = (df["nombre"].groupby(df["date"].dt.hour)).plot(kind="bar")
    plt.xticks(np.arange(len(df)), [str(e.month)+" / "+str(e.year) for e in df["date"]] )
    plt.show()


# +
#Afficher tous les matchs d'une période pour un joueur 

def matchs_period(con, joueur, debut, fin):
    
    taper_votre_joueur = joueur

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]
    print(id_joueur)

    for row in con.execute("select distinct name, date from tournois join match on tournois.id = match.tournoi where match.white_player = ? or match.black_player =?", (id_joueur, id_joueur, )):
        if is_in_period(debut, fin, row[1]):
            print(row[0])


# +
#Pour un tournoi auquel il a participé donner les infos

def infos_joueur_tournoi(con, joueur, tournoi):
    taper_votre_joueur = joueur

    id_joueur = list(con.execute("select id from player where name = ?", (taper_votre_joueur,)))[0][0]
    print(id_joueur)
    
    id_tournoi = list(con.execute("select id from tournois where name = ?", (tournoi,)))[0][0]
    print(id_tournoi)

    #for row in con.execute("select white_player, black_player, winner from match join tournois on tournois.id = match.tournoi where tournois.id = ? and (match.white_player = ? or match.black_player =?)", (id_tournoi, id_joueur, id_joueur, )):
         #print(row) 
            
            
            
    for row in con.execute("select p1.name, p2.name, m2.winner from player p1, player p2, match m2 join match m1 on m2.id = m1.id and m1.black_player=p1.id and m1.white_player = p2.id join tournois on tournois.id = m1.tournoi where tournois.id = ? and (m1.white_player = ? or m1.black_player =?)", (id_tournoi, id_joueur, id_joueur, )):
        if row[2]==0:
            print(row[0]+ " contre " + row[1]+ " ------>  " + "winner (noir) : "+row[0])  
        if row[2]==1:
            print(row[0]+ " contre " + row[1]+ " ------>  " + "winner (blanc) : "+row[1]) 
        if row[2]==2:
            print(row[0]+ " contre "+ row[1]+ " ------>  " + "winner : ex aequo ") 
    
# -


