# RECUPERATION DES DONNES POUR UNE GRILLE BERGER

import requests
from bs4 import BeautifulSoup

def recup_berger(number):#number=numéro d'une grille berger
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




#checker si la page est américaine 
def american(number):
    link = f"http://echecs.asso.fr/Resultats.aspx?URL=Tournois/Id/{number}/{number}&Action=Ga"
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    for x in soup.find_all('span'):
        if x.string == "Désolé, le fichier n'existe pas...":
            print("berger")
            return False
        else :
            print("américain")
            return True 


#pour avoir la date, le nom, la cadence, et les rondes du tournoi
def infos_tournoi(number):  
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



from datetime import datetime

# datetime(2021, 3, 14) #année, mois, jour 

months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}

def stop_boucle(date): #fonction qui renvoie true si on est après la date d'aujourd'hui
    months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}
    liste_date = date.strip('-').split(' ')
    if liste_date[0]=='' and liste_date[1]=='-' and liste_date[2]=='':
        return False 
    jour = liste_date[1] #6
    mois = months[liste_date[2]] #7
    année = liste_date[3] #8
   
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

def is_in_period(debut, fin, date): #renvoie True quand on est bien dans cette période là
    #debut et fin sont en format datetime
    months = {"janvier":1, "février":2, "mars":3, "avril":4,
       "mai":5, "juin":6, "juillet":7, "août":8,
       "septembre":9, "octobre":10, "novembre":11, "décembre":12}
    liste_date = date.strip('-').split(' ')
    if liste_date[0]=='' and liste_date[1]=='-' and liste_date[2]=='':
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
    elif int(année_debut)==int(debut.year):
        if int(mois_debut)<int(debut.month):
            return False
        elif int(mois_debut)==int(debut.month):
            if int(jour_debut)<int(debut.day):
                return False
    return True

# print(stop_boucle('mercredi 23 juin 2022 - samedi 8 juillet 2022'))

def date_debut(date): 
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






def players_ga(number):
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
        if a==17 :
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" :
                    res.append(x.string)
        elif a==18:
            col='rien'
            for (k,x) in enumerate(soup.find_all('td')) :
                if x.has_attr("class") and x["class"][0]=="papi_l" and k==19 :
                    col = x.string
            if col=='Cu.' or col=="Bu." or col == "Perf" or col=="NV":
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
                if x.has_attr("class") and x["class"][0]=="papi_l" and (k-23)%a==0:
                    res.append(x.string)
                  
        res = res[1:]
        indicateur = 2
                     
    return (res, indicateur)


def match_ga(number):
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




def insere_ga(number, con):
    #inserer le tournoi
    date_tournoi = infos_tournoi(number)["date"]
    nom_tournoi = infos_tournoi(number)["nom"]
    nb_rondes_tournoi = infos_tournoi(number)["nb_rondes"]
    if "cadence" in infos_tournoi(number):
        cadence_tournoi = infos_tournoi(number)["cadence"]
        con.execute("insert into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?, ?)",(number, nom_tournoi, date_tournoi, nb_rondes_tournoi, cadence_tournoi, "américain",))   
    else :
        con.execute("insert into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?,?)",(number, nom_tournoi, date_tournoi, nb_rondes_tournoi, "aucun", "américain",))
        
    #inserer les joueurs du tournoi
    players, ind = players_ga(number)
    print(players)
    for player in players:
        p = player.lower()
        recherche = list(con.execute("select name from player where name = ?", (p,)))
        if recherche == []:
            con.execute("insert into player(name) values (?)", (player.lower(),))
    
    #inserer les matchs du tournoi
    for element in match_ga(number):
        #id_tournoi = list(con.execute("select id from tournois where name = ?", (nom_tournoi,)))[0][0]
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



                

                

def insertion_berger(number, con):#number=numéro du tournoi
    #insertion des joueurs du tournoi
    for player in recup_berger(number)[0]:
        recherche = list(con.execute("select name from player where name = ?", (player.lower(),)))
        if player not in recherche:
            con.execute("insert into player(name) values (?)",(player.lower(),))
    #insertion dans la table tournois 
    if "cadence" in infos_tournoi(number):
        con.execute("insert or replace into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?, ?)",(number, infos_tournoi(number)["nom"],infos_tournoi(number)["date"],infos_tournoi(number)["nb_rondes"],infos_tournoi(number)['cadence'], "berger",))   
    else :
        con.execute("insert or replace into tournois(id, name, date, rondes, cadence, type) values(?,?,?,?,?,?)",(number, infos_tournoi(number)["nom"],infos_tournoi(number)["date"],infos_tournoi(number)["nb_rondes"],"aucun", "berger", ))
    
    #insertion des matchs d'un tournoi
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

        

def database(number_min, number_max, con):
    #18324
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


