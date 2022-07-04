# # Fonctions utiles pour construire la base de données

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def american(number):
    
    
    
    '''
    Retourne True si la grille est de type américaine et False si elle est de type berger.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site

            Retourne:
                    (bool): True si grille américaine et False si griller berger
    '''
    
    
    
    
    link = f"http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{number}/{number}&Action=Ga"
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    
    for x in soup.find_all('span'):
        if x.string == "Désolé, le fichier n'existe pas...":
            print("berger")
            return False
        else :
            print("américain")
            return True 


def infos_tournoi(number): 
    
    
    
    '''
    Retourne le nom, la date, le nombre de rondes et la cadence d'un tournoi.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site

            Retourne:
                    infos (dict): Dictionnaire avec comme clés la date, le nom, le nombre de rondes et la cadence du tournoi
    '''
    
    
    
    infos = dict()
    link_infos = f"http://echecs.asso.fr/FicheTournoi.aspx?Ref={number}"
    soup_infos = BeautifulSoup(requests.get(link_infos).text, 'html.parser')
    
    for x in soup_infos.find_all('span'):
        if x.has_attr("id") and x['id'] == "ctl00_ContentPlaceHolderMain_LabelDates":
            infos["date"] = x.string   
        if x.has_attr("id") and x['id'] == "ctl00_ContentPlaceHolderMain_LabelNom":
            infos["nom"] = x.string  
        if x.has_attr("id") and x['id'] == "ctl00_ContentPlaceHolderMain_LabelNbrRondes":
            infos["nb_rondes"] = x.string
        if x.has_attr("id") and x['id'] == "ctl00_ContentPlaceHolderMain_LabelCadence":
            infos["cadence"] = x.string 
    return infos


def stop_boucle(date): 
    
    
    '''
    Retourne True si on doit arrêter la boucle car date se situe après la date d'aujourd'hui.

            Paramètres:
                    date (str): Une chaîne de caractère représentant une période sur laquelle se déroule un tournoi.

            Retourne:
                    (bool): True si on doit arrêter la boucle et False si on peut la continuer.
    '''
    
    
    months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}
    
    
    liste_date = date.strip('-').split(' ')
    if liste_date[0]=='' and liste_date[1]=='-' and liste_date[2]=='': #la date est vide
        return False 
    
    jour = liste_date[1]
    mois = months[liste_date[2]] 
    année = liste_date[3] 
   
    jour_now, mois_now, année_now = datetime.today().day, datetime.today().month, datetime.today().year
    
    if int(année)>int(année_now):
        return True
    elif int(année)==int(année_now):
        if int(mois)>int(mois_now):
            return True
        elif int(mois)==int(mois_now):
            if int(jour)>int(jour_now):
                return True
    return False

def is_in_period(debut, fin, date): 
    
    '''
    Retourne True si date se situe dans la période debut-fin.

            Paramètres:
                    debut (datetime): Une date de début sous format datetime
                    fin(datetime): Une date de fin sous format datetime
                    date(str): Une chaîne de caractère représentant une période sur laquelle se déroule un tournoi.

            Retourne:
                    (bool): True si la date du tournoi est bien dans la période debut-fin et False sinon.
    '''
    
    
    
    months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}
    
    
    liste_date = date.strip('-').split(' ')
    if liste_date[0]=='' and liste_date[1]=='-' and liste_date[2]=='': #date vide
        return True  
    
    jour_debut = liste_date[1]
    mois_debut = months[liste_date[2]]
    annee_debut = liste_date[3]
    jour_fin = liste_date[6]
    mois_fin = months[liste_date[7]]
    annee_fin = liste_date[8]
    if int(annee_fin)>int(fin.year) or int(annee_debut)<int(debut.year):
        return False
    elif int(annee_fin)==int(fin.year):
        if int(mois_fin)>int(fin.month):
            return False
        elif int(mois_fin)==int(fin.month):
            if int(jour_fin)>int(fin.day):
                return False
    elif int(annee_debut)==int(debut.year):
        if int(mois_debut)<int(debut.month):
            return False
        elif int(mois_debut)==int(debut.month):
            if int(jour_debut)<int(debut.day):
                return False
    return True


def date_debut(date): 
    
    '''
    Retourne la date de début du tournoi se déroulant à la période date.

            Paramètres:
                    date(str): Une chaîne de caractère représentant une période sur laquelle se déroule un tournoi.

            Retourne:
                    jour_debut (int): le jour du début du tournoi
                    mois_debut(int) : le numéro du mois du début du tournoi
                    liste_date[2] (str) : le nom du mois du début du tournoi
                    annee_debut (int) : l'année du début du tournoi
    '''
    
    
    months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}
    
    
    liste_date = date.strip('-').split(' ')
    if liste_date[0]=='' and liste_date[1]=='-' and liste_date[2]=='':
        return None 
    jour_debut = liste_date[1]
    mois_debut = months[liste_date[2]]
    annee_debut = liste_date[3]
    return (jour_debut, mois_debut, liste_date[2], annee_debut)


def recup_berger(number):
    
    '''
    Retourne les joueurs, les elos et les matchs d'une grille berger.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site
            
            Retourne:
                    joueur (list): liste des joueurs du tournoi
                    elo(dict) : dictionnaire avec les noms des joueurs comme clés et les elos des joueurs comme valeurs
                    dictionnaire (dict) : dictionnaire avec les noms des joueurs comme clés et comme valeur un dictionnaire avec les scores des matchs pour chaque adversaire
                        
    '''
    
    link = f"http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{number}/{number}&Action=Berger"
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    
    #récupération des joueurs
    j=[]
    for x in soup.find_all('td'):
        if x.has_attr("class") and x['class'][0] == "papi_border_l" :
            j.append(x.string.lower())
    joueur=j[1:]
    
    #trouver taille du tableau:a
    for k,x in enumerate(soup.find_all('tr')):
        if x.has_attr("class") and x['class'][0] == "papi_liste_c":
            if k==1:
                a=0
                for y in x.find_all('td'):
                    a+=1
    
    
    #récupération des elo
    e=[]
    i=0
    for x in soup.find_all('tr'):
        if x.has_attr("class") and x['class'][0] == "papi_liste_c":
            for k,y in enumerate(x.find_all('td')):
                if (k-3)%a==0 and k!=1 and i<len(joueur)+1:
                    z=str(y.string).split("\xa0")
                    if len(z)==2:
                        elo = z[0]+z[1]
                    else :
                        elo = z[0]
                    e.append(elo)
                    i+=1
    elo=dict()
    for i in range(len(joueur)):
        elo[joueur[i]]=e[1:][i]
    
    
    #récupération des scores relatifs sous forme de dictionnaire
    dic=dict()
    for i in range(len(joueur)):
        p=[]
        for x in soup.find_all('tr'):
            if x.has_attr("class") and x['class'][0] == "papi_liste_c":
                for k,y in enumerate(x.find_all('td')):
                    if (k-4-i)%a==0:
                        p.append(y.string)
        perf_colonne=p[1:len(joueur)+1]
        dic[joueur[i]]=perf_colonne
        #avant on a récupéré tous les modulos 15, ie on a les scores en colonne, on doit les présenter en ligne   
    
    dictionnaire=dict()
    for i in range(len(joueur)):
        dico_joueur=dictionnaire[joueur[i]]= dict()
        for j in range(len(joueur)):
            if j!=i:
                dico_joueur[joueur[j]]=dic[joueur[j]][i]
    
    return(joueur,elo,dictionnaire)       


def players_ga(number):
    
    '''
    Retourne les joueurs d'une grille berger.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site
            
            Retourne:
                    res (list) : La liste des joueurs du tournoi
                    ind(int) : 1 si la présentation de la page est nouvelle et 2 si elle est ancienne
    '''
    
    
    indicateur = 0
    res = []
    link = f"http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{number}/{number}&Action=Ga"
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    for x in soup.find_all('div'):
        if x.has_attr("class") and x['class'][0] == "papi_joueur_box":
            res.append(x.b.string)
    indicateur = 1
        
    if res == []:
        for k,x in enumerate(soup.find_all('tr')):
            if x.has_attr("class") and x['class'][0] == "papi_small_t":
                a=0
                for y in x.find_all('td'):
                    a+=1
        if a==18:
            col='rien'
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" and k==19 :
                    col = x.string
                    
            if col=='Cu.' or col=="Bu." or col == "Perf" or col =="NV" or col=='Ko.' or col=='Me.' or col=='Tr.':
                for (k,x) in enumerate(soup.find_all('td')) :
                    if x.has_attr("class") and x["class"][0]=="papi_l" and (k-23)%a==0:
                        res.append(x.string)
                        
            else:
                for (k,x) in enumerate(soup.find_all('td')) :
                    if x.has_attr("class") and x["class"][0]=="papi_l" :
                        res.append(x.string)
                    
        
        elif a==20:
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" :
                    indice = k
                
                    break
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" and (k-(a+indice))%a==0 :
                    res.append(x.string)
               
    
        else :
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" and (k-(5+a))%a==0:
                    res.append(x.string)
              
            if res==[]:
                for (k,x) in enumerate(soup.find_all('td')) :
                    if x.has_attr("class") and x["class"][0]=="papi_l" :
                        res.append(x.string)
                 
        res = res[1:]
        indicateur = 2
                     
    return (res, indicateur)


def match_ga(number):
    
    '''
    Retourne les matchs d'une grille américaine (adversaires, elos, gagnant).

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans 
                    le site
            
            Retourne:
                    res (list) : liste dont chaque élément est une liste contenant 
                    les deux joueurs, leurs elos, la couleur jouée par le premier, 
                    et 1 si le premier a gagné, 1/2 si égalité et 0 s'il a perdu. 
    '''
    
    
    symboles = ['+', '-', "=", ">", "<"]
    players, ind = players_ga(number)
    link = f"http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{number}/{number}&Action=Ga"
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    
    res = []

    if ind== 1:
        adversaires = []
        elos = []
        couleurs = []
        résultats = []
        for x in soup.find_all('div'):
            if x.has_attr("class") and x.has_attr("align") and x['align'] == "center":
                joueur = []
                elo = []
                couleur = []
                résultat = []
                for k,y in enumerate(x.find_all('td')):
                    if (k-16)%13==0:
                        joueur.append(y.string)
                    if (k-17)%13==0:
                        z=str(y.string).split("\xa0")
                        elo.append(z)
                    if (k-12)%13==0:
                        couleur.append(y.string)
                    if k%13==0:
                        résultat.append(y.string)
                adversaires.append(joueur) 
                elos.append(elo)
                couleurs.append(couleur)
                résultats.append(résultat)
    if ind == 2:
        adversaires = []
        elos = []
        couleurs = []
        résultats = []
        for j,x in enumerate(soup.find_all('tr')):
            if j>2 and (j-3)<len(players):
                joueur = [players[j-3]]
                elo = []
                couleur = []
                résultat = []
                for k,y in enumerate(x.find_all('td')):
                    if y.has_attr("class") and (y['class'][0] == "papi_r" or y['class'][0] == "papi_c"):
                        if k==3:
                            z=str(y.string).split("\xa0")
                            elo.append(z)
                        if y.string!=None and y.string[0] in symboles and len(y.string)>4:
                            truc = y.string[:-1].split('\xa0')
                            if len(truc)>=2:
                                joueur.append(players[int(truc[-1])-1])
                                couleur.append(y.string[-1])
                                résultat.append(truc[0])
                            else : 
                                joueur.append(players[int(truc[0][1:])-1])
                                couleur.append(y.string[-1])
                                résultat.append(truc[0][0])
                        elif y.string!=None and y.string[0] in symboles and y.string[-1] in ['B', 'N'] and len(y.string)<=4:
                            
                            joueur.append(players[int(y.string[1:-1])-1])
                            couleur.append(y.string[-1])
                            résultat.append(y.string[0])
                adversaires.append(joueur) 
                elos.append(elo)
                couleurs.append(couleur)
                résultats.append(résultat)

    déjà_vus = set()
    if ind==1:
        for k in range (len(adversaires)):
            for i in range(1,len(adversaires[k])):
                match = []
                try:
                    match.append(adversaires[k][0])
                    déjà_vus.add(adversaires[k][0])
                    match.append(adversaires[k][i])
                    match.append(elos[k][0])
                    match.append(elos[k][i])
                    match.append(couleurs[k][i-1])
                    match.append(résultats[k][i])
                    if adversaires[k][i] not in déjà_vus:
                        res.append(match)
                except IndexError:
                    pass
    if ind ==2:
        for k in range (len(adversaires)):
            for i in range(1,len(adversaires[k])):
                match = []
                match.append(adversaires[k][0])
                déjà_vus.add(adversaires[k][0])
                match.append(adversaires[k][i])
                match.append(elos[k][0])
                match.append(elos[players.index(adversaires[k][i])][0])
                match.append(couleurs[k][i-1])
                match.append(résultats[k][i-1])
                if adversaires[k][i] not in déjà_vus:
                    res.append(match)
    return res


def insertion_berger(number, con):
    
    '''
    Insère un tournoi de type berger dans la base de donnée appelée par con.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    
                    
            Retourne:
                    None
    '''
    
    
    #insertion des joueurs dans la table player
    for player in recup_berger(number)[0]:
        recherche = list(con.execute("select name from player where name = ?", (player.lower(),)))
        if player not in recherche:
            con.execute("insert into player(name) values (?)",(player.lower(),))
    
    
    
    #insertion du tournoi dans la table tournois 
    if "cadence" in infos_tournoi(number):
        con.execute("insert or replace into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?, ?)",(number, infos_tournoi(number)["nom"],infos_tournoi(number)["date"],infos_tournoi(number)["nb_rondes"],infos_tournoi(number)['cadence'], "berger",))   
    else :
        con.execute("insert or replace into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?,?)",(number, infos_tournoi(number)["nom"],infos_tournoi(number)["date"],infos_tournoi(number)["nb_rondes"],"aucun", "berger", ))
    
    
    
    #insertion des matchs dans la table match
    i=0
    for player in recup_berger(number)[0]:
        dicomatch=recup_berger(number)[2]
        dicojoueur=dicomatch[player]
        joueurrestant=list(dicojoueur.keys())[i:]
        for adversaire in joueurrestant:
            black_id = list(con.execute("select id from player where name = ?", (player.lower(),)))[0][0]
            white_id = list(con.execute("select id from player where name = ?", (adversaire.lower(),)))[0][0]
            elo_black=recup_berger(number)[1][player]
            elo_white=recup_berger(number)[1][adversaire]
            if dicojoueur[adversaire]=='1':
                winner=0
            if dicojoueur[adversaire]=='0':
                winner=1
            else:
                winner=2
            con.execute("insert or replace into match(tournoi,black_player,elo_black,white_player,elo_white,winner) values(?,?,?,?,?,?)",(number,black_id,elo_black,white_id,elo_white,winner,))    
        i+=1


def insere_ga(number, con):
    
    '''
    Insère un tournoi de type américain dans la base de donnée appelée par con.

            Paramètres:
                    number (int): Un entier représentant le numéro du tournoi dans le site
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    
                    
            Retourne:
                    None
    '''
    
    
    #insertion du tournoi dans la table tournois 
    date_tournoi = infos_tournoi(number)["date"]
    nom_tournoi = infos_tournoi(number)["nom"]
    nb_rondes_tournoi = infos_tournoi(number)["nb_rondes"]
    if "cadence" in infos_tournoi(number):
        cadence_tournoi = infos_tournoi(number)["cadence"]
        con.execute("insert into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?, ?)",(number, nom_tournoi, date_tournoi, nb_rondes_tournoi, cadence_tournoi, "américain",))   
    else :
        con.execute("insert into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?,?)",(number, nom_tournoi, date_tournoi, nb_rondes_tournoi, "aucun", "américain",))
        
        
        
    #insertion des joueurs dans la table player
    players, ind = players_ga(number)
    for player in players:
        p = player.lower()
        recherche = list(con.execute("select name from player where name = ?", (p,)))
        if recherche == []:
            con.execute("insert into player(name) values (?)", (player.lower(),))
    
    
    
    #insertion des matchs dans la table match
    for element in match_ga(number):
        
        if element[1]!= 'EXEMPT' and element[1]!=None and element[0]!='EXEMPT' and element[0]!=None:
            p_1 = list(con.execute("select id from player where name = ?", (element[0].lower(),)))
            p_2 = list(con.execute("select id from player where name = ?", (element[1].lower(),)))
            if p_1!=[] and p_2!=[]:
                player_1 = list(con.execute("select id from player where name = ?", (element[0].lower(),)))[0][0]
                player_2 = list(con.execute("select id from player where name = ?", (element[1].lower(),)))[0][0]
                if len(element[2])==2 :
                    elo_1 = element[2][0]+element[2][1]
                else :
                    elo_1 = element[2][0]
                if len(element[3])==2:
                    elo_2 = element[3][0]+element[3][1]
                else :
                    elo_2 = element[3][0]
                if element[4] == 'N':
                    black_player = player_1
                    elo_black = elo_1
                    white_player = player_2
                    elo_white = elo_2
                    if element[5]=='1' or element[5]=='+' :
                        winner = 0
                    elif element[5]=='½' or element[5]=="=":
                        winner = 2
                    elif element[5]=='0' or element[5]=='-':
                        winner = 1 
                    elif element[5]=='>':
                        winner = 3
                    elif element[5]=='<':
                        winner = 4
                else :
                    white_player = player_1
                    elo_white = elo_1
                    black_player = player_2
                    elo_black = elo_2
                    if element[5]=='1' or element[5]=='+' :
                        winner = 1
                    elif element[5]=='½' or element[5]=="=":
                        winner = 2
                    elif element[5]=='0' or element[5]=='-':
                        winner = 0
                    elif element[5]=='>':
                        winner = 4
                    elif element[5]=='<':
                        winner = 3
                con.execute("insert into match(tournoi, black_player, elo_black, white_player, elo_white, winner) values (?,?,?,?,?,?)", (number, black_player, elo_black, white_player, elo_white, winner))


def database(number_min, number_max, con):
    
    '''
    Remplit la base de donnée appelée par con par les tournois numérotés de number_min
    à number_max.

            Paramètres:
                    number_min (int): Un entier représentant le numéro du premier tournoi à ajouter
                    number_max (int): Un entier représentant le numéro du dernier tournoi à ajouter
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    
                    
            Retourne:
                    None
    '''
    
    
    number = number_min
    while number<number_max:
        number+=1
        print(number)
        try:
            if not stop_boucle(infos_tournoi(number)['date']):
                if american(number):
                    try:
                        insere_ga(number, con)
                    except UnboundLocalError as e:
                        print(e)
                    except IndexError as a:
                        print(a)
                else :
                    insertion_berger(number, con)
        except KeyError as e:
            print(e)           


def update(number_max, con):
    
    
    '''
    Update la base de donnée appelée par con jusqu'à aujourd'hui.

            Paramètres:
                    number_max (int): Un entier très grand comme borne sup pour la boucle while.
                    con (sqlite3.Connection): Une connexion à une base de donnée
                    
                    
            Retourne:
                    None
    '''
    
    
    for row in con.execute("select id from tournois order by id desc limit 1"):
        last = row[0]
    database (last, number_max, con)


