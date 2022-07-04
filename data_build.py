# # Remplissage de la base de données

import sqlite3
from chess_functions import *
from stats import *

# Création de la base de donnée

con = sqlite3.connect('MyDataBase.db')

# Création des tables

con.executescript("""
create table player (id integer not NULL primary key autoincrement, name text not NULL); 
create table tournois (id integer not NULL primary key autoincrement, name text, date text, rondes integer, cadence string, type string);
create table match (id integer primary key autoincrement, tournoi integer, black_player integer, elo_black string, white_player integer, elo_white string, winner integer);""")

# Remplissage de la base de données

database(18324,60000, con)

# Enregistrement des ajouts 

con.commit()


# Visualisation de la base de données

# +
for row in con.execute("select * from match"):
    print(row)
    
for row in con.execute("select * from player"):
    print(row)
    
for row in con.execute("select * from tournois"):
    print(row)
