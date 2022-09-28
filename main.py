import pandas as pd
import auxiliar as aux
import json

f = open("data.json")

dados = json.load(f)

titulo_albuns = [aux.tira_parenteses(x) for x in dados]

print(" ".join(titulo_albuns))
# for album in dados:
#     print(album)

f.close()