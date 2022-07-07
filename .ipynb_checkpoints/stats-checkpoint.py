# # Fonctions utiles pour faire des statistiques

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from chess_functions import *


def actif(con):
    
    
    '''
    Retourne le nom du joueur qui a joué le plus de matchs dans la base de données.
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée

            Retourne:
                    nom_joueur(str): Nom du joueur qui a joué le plus de matchs
                    
    '''
    
    actif = 0
    max = 0
    
    for player in con.execute("select id from player"):
        longueur = len(list(con.execute("select tournoi from match where white_player = ? or black_player =?", (player[0],player[0],))))
        if longueur>max :
            max = longueur
            actif = player[0]
    
    nom_joueur = list(con.execute("select name from player where id = ?", (actif,)))[0][0]
    print(nom_joueur, actif)
    print(max)
    return nom_joueur


def victoire_couleur(joueur, con):
    
    
    '''
    Trace l'histogramme des défaites, victoires et matchs nuls selon la couleur 
    jouée par le joueur.
    
            Paramètres:
                    joueur(str): Nom du joueur
                    con (sqlite3.Connection): Une connexion à une base de donnée

            Retourne:
                    None
                    
    '''

    hist = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]
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

    df = pd.DataFrame.from_dict(hist, orient='index')
    df.plot(kind='bar')
    plt.title("Victoires, nuls et défaites de " + joueur + " selon la couleur jouée")
    plt.show()


def elo_evolution(con, joueur):
    
    
    '''
    Trace le graphe de l'évolution du elo du joueur en fonction du numéro du tournoi.
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    joueur(str): Nom du joueur

            Retourne:
                    None
                    
    '''
    
    
    tournoi = []
    elo = []

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]

    for row in list(con.execute("select tournoi,elo_black from match where black_player =?", (id_joueur,))):
        if not row[0] in tournoi:
            tournoi.append(row[0])
            if type(row[1])== int:
                elo.append(row[1])
            else :
                elo.append(int(row[1][:-1]))
            
    for row in list(con.execute("select tournoi,elo_white from match where white_player =?", (id_joueur,))):
        if not row[0] in tournoi:
            tournoi.append(row[0])
            if type(row[1])== int:
                elo.append(row[1])
            else :
                elo.append(int(row[1][:-1]))

    plt.plot(tournoi, elo)
    plt.title("Evolution du elo de " + joueur + " en fonction des tournois")
    plt.show()


def top_adversaires(con, joueur):

    
    '''
    Trace l'histogramme des adversaires rencontrés 2 fois ou plus, 
    la couleur représentant la défaite, le nul ou la victoire.
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    joueur(str): Nom du joueur

            Retourne:
                    None
                    
    '''
    
    
    dico = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]
    print(id_joueur)

    for row in con.execute("select player.name, match.winner from player join match on player.id = match.black_player where match.white_player = ?", (id_joueur, )):
        #le joueur joue blanc
        adversaire = row[0]
        winner = row[1]
        
        if winner ==3:
            winner =  0
        elif winner ==4:
            winner = 1
            
        if adversaire not in dico.keys():
            dico[adversaire]=[winner]
        else :
            dico[adversaire].append(winner)
        
    for row in con.execute("select player.name, match.winner from player join match on player.id = match.white_player where match.black_player = ?", (id_joueur, )):
        #le joueur joue noir
        adversaire = row[0]
        winner = row[1]
        
        if winner == 0: 
            winner = 1
        elif winner == 1:
            winner = 0
        elif winner ==3:
            winner =  1
        elif winner ==4:
            winner = 0
            
        if adversaire not in dico.keys():
            dico[adversaire]=[winner]
        else :
            dico[adversaire].append(winner)
            
    adversaires = dict()
    adversaires_normalized = dict()
    
    i=0
    for key in dico.keys(): #mettre seulement les adversaires qu'il a vus plusieurs fois 
        if len(dico[key])>1:
            victoire = sum([e for e in dico[key] if e!=2])
            nul = sum([1 for e in dico[key] if e==2])
            adversaires[i]=[key, victoire, nul, len(dico[key])-victoire - nul] #nombre de réussites, nombre de nuls, nombre de défaites
            adversaires_normalized[i] = [key, victoire/len(dico[key]), nul/len(dico[key]), 1-victoire/len(dico[key]) - nul/len(dico[key])] #taux de réussites, taux de nuls, taux de défaites 
            i+=1

    df = pd.DataFrame.from_dict(adversaires, orient='index', columns = ["adversaire", "réussite", "nul", "défaite"])
    df_normalized = pd.DataFrame.from_dict(adversaires_normalized, orient='index', columns = ["adversaire", "réussite", "nul", "défaite"])
    
    df.plot(x="adversaire", y=["réussite", "nul", "défaite"], kind="bar", color = ['g', 'orange', 'red'], stacked=True, label=['Nombre de réussite', 'Nombre de nul', 'Nombre de défaite'], figsize=(20, 10)) 
    plt.xlabel('Adversaires')
    plt.title('Tableau des réussites, nuls et défaites de '+joueur+' (non normalisé)')
    plt.xticks(np.arange(len(df)), [e for e in df["adversaire"]]) 
    plt.show()
    
    df_normalized.plot(x="adversaire", y=["réussite", "nul", "défaite"], kind="bar", color = ['g', 'orange', 'red'], stacked=True, label=['Taux de réussite', 'Taux de nul', 'Taux de défaite'], figsize=(20, 10)) 
    plt.xlabel('Adversaires')
    plt.title('Tableau des réussites, nuls et défaites de '+joueur+' (normalisé)')
    plt.xticks(np.arange(len(df_normalized)), [e for e in df_normalized["adversaire"]]) 
    plt.show()


def number_match(con, joueur):
    
    
    '''
    Trace l'histogramme du nombre de tournois auxquels le joueur a participés par mois. 
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    joueur(str): Nom du joueur

            Retourne:
                    None
                    
    '''
    
    
    matchs = dict()

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]
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
    plt.title("Nombre de tournois joués par " + joueur + " par mois")
    plt.show()


def matchs_period(con, joueur, debut, fin):
    
    
    '''
    Retourne la liste des tournois auxquels le joueur a participé dans la période debut-fin.
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    joueur(str): Nom du joueur
                    debut(datetime): date du début de la période au format datetime
                    fin(datetime): date de la fin de la période au format datetime
                    

            Retourne:
                    tournois (list):liste des tournois participés dans la période debut-fin.
                    
    '''
    
    tournois = []

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]
    print(id_joueur)

    for row in con.execute("select distinct name, date from tournois join match on tournois.id = match.tournoi where match.white_player = ? or match.black_player =?", (id_joueur, id_joueur, )):
        if is_in_period(debut, fin, row[1]):
            print(row[0])
            tournois.append(row[0])
            
    return tournois 


def infos_joueur_tournoi(con, joueur, tournoi):
    
    
    '''
    Retourne, pour ce tournoi, la liste des matchs impliquant le joueur avec leur issue.
    
            Paramètres:
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    joueur(str): Nom du joueur
                    tournoi(str): Nom du tournoi 


            Retourne:
                    res (list):liste de dictionnaires contenant les deux adversaires, 
                    la couleur du gagnant, et le nom du gagnant.
                    
    '''
    
    res = []

    id_joueur = list(con.execute("select id from player where name = ?", (joueur,)))[0][0]
    print(id_joueur)
    
    id_tournoi = list(con.execute("select id from tournois where name = ?", (tournoi,)))[0][0]
    print(id_tournoi)

    for row in con.execute("select p1.name, p2.name, m2.winner from player p1, player p2, match m2 join match m1 on m2.id = m1.id and m1.black_player=p1.id and m1.white_player = p2.id join tournois on tournois.id = m1.tournoi where tournois.id = ? and (m1.white_player = ? or m1.black_player =?)", (id_tournoi, id_joueur, id_joueur, )):
        if row[2]==0:
            print(row[0]+ " contre " + row[1]+ " ------>  " + "winner (noir) : "+row[0])
            match = {"j1" : row[0], "j2": row[1], "winner_color" : "noir", "winner":row[0]}
            res.append(match)
        if row[2]==1:
            print(row[0]+ " contre " + row[1]+ " ------>  " + "winner (blanc) : "+row[1]) 
            match = {"j1" : row[0], "j2": row[1], "winner_color" : "blanc", "winner":row[1]}
            res.append(match)
        if row[2]==2:
            print(row[0]+ " contre "+ row[1]+ " ------>  " + "winner : ex aequo ") 
            match = {"j1" : row[0], "j2": row[1], "winner_color" : None, "winner": "ex aequo"}
            res.append(match)
    return res



