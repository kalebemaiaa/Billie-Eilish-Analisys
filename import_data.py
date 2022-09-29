"""
    Este arquivo serve para importar a base da dos utilizada para fazer as análises.
"""
import time
import requests
import pandas as pd

# API DEEZER
dados_artista = requests.get("https://api.deezer.com/artist/9635624")
dados_tracklist = requests.get(dados_artista.json()["tracklist"])

musicas_data = dados_tracklist.json()["data"]

estrutura_musicas = [{"album": music["album"]["title"].upper(),
                      "duracao": music["duration"],
                      "rank": music["rank"],
                      "nome":music["title"].upper()} for music in musicas_data]

pd.DataFrame(estrutura_musicas).to_csv("dados_musicas.csv")

# API VAGALUME
# LINK: https://www.vagalume.com.br/


KEY_APY = "a829b6e84397c7592f558d850b888203"
ARTISTA = "billie-eilish"

requisicao_artista = requests.get(
    "https://www.vagalume.com.br/" + ARTISTA + "/index.js")

dados_artista = requisicao_artista.json()

musicas = [x for x in dados_artista["artist"]["lyrics"]["item"]]
letras = []

for song in musicas:
    url = "https://api.vagalume.com.br/search.php?musid=" + \
        song["id"] + "&apikey=" + KEY_APY
    requisicao = requests.get(url)
    try:
        letras.append({"letra": requisicao.json()["mus"][0]["text"].upper(),
                       "nome": requisicao.json()["mus"][0]["name"].upper()})
    except requests.exceptions.JSONDecodeError:
        print(requisicao, "\t-> RESTART MUITAS REQUISICOES")
        time.sleep(10)
        requisicao = requests.get(url)

        letras.append({"letra": requisicao.json()["mus"][0]["text"].upper(),
                       "nome": requisicao.json()["mus"][0]["name"].upper()})
    else:
        print(requisicao)

pd.DataFrame(letras).to_csv("dados_letras.csv")
