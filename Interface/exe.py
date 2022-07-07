#  # #!/usr/bin/env python

# +
import sys
from stats import *
import json
from datetime import datetime

import sqlite3
from chess_functions import *
from stats import *

con = sqlite3.connect('MyDataBase.db')


if len(sys.argv) != 5:
    print("Python code input error")
    exit(1)

name = sys.argv[1]
surname = sys.argv[2]
first_day = sys.argv[3]
last_day = sys.argv[4]

def conv_date(dt):
    lst=dt.split('/')
    return datetime(int(lst[2]),int(lst[1]),int(lst[0]))


try :
    res = matchs_period(con, surname.lower()+' '+name.lower(), conv_date(first_day), conv_date(last_day))
    dico = {f"item_{i}":res[i] for i in range(len(res))}
    with open ('output.json', "w") as output_file:
          json.dump(dico, output_file)
except IndexError as i :
    res = []
    dico = {f"item_{i}":res[i] for i in range(len(res))}
    with open ('output.json', "w") as output_file:
        json.dump(dico, output_file)
  


#TODO: RENVOYER UNE LISTE VIDE ET ÉCRIRE UN DICO VIDE QUAND LA PERSONNE N'EST PAS TROUVÉE

with open ('output.json', "w") as output_file:
    json.dump(dico, output_file)
# -

print("Player name: {0}, Last name: {1}, First day: {2}, Last day: {3}".format(name,surname,first_day,last_day))
