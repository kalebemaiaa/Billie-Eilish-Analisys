"""
    Este arquivo serve para importar a base da dos utilizada para fazer as análises.
"""

import json
import time
import requests
import auxiliar as aux

#API DEEZER
dados_artista = requests.get("https://api.deezer.com/artist/9635624")
dados_tracklist = requests.get(dados_artista.json()["tracklist"])

musicas_data = dados_tracklist.json()["data"]

dicionario = {}

for musica in musicas_data:
    album = musica["album"]["title"]

    try:
        estrutura = {
            musica['title'].upper():{
                "duracao": musica["duration"],
                "rank" : musica["rank"]
            }
        }
        dicionario[album.upper()].append(estrutura)
    except KeyError:
        dicionario[album.upper()] = []
        estrutura = {
            musica['title'].upper():{
                "duracao": musica["duration"],
                "rank" : musica["rank"]
            }
        }
        dicionario[album.upper()].append(estrutura)

#API VAGALUME
KEY_APY = "a829b6e84397c7592f558d850b888203"
ARTISTA = "billie-eilish"

requisicao_artista = requests.get("https://www.vagalume.com.br/" + ARTISTA + "/index.js")

dados_artista = requisicao_artista.json()

musicas = [x for x in dados_artista["artist"]["lyrics"]["item"]]
letras = []

for song in musicas:
    url = "https://api.vagalume.com.br/search.php?musid=" + song["id"] + "&apikey=" + KEY_APY
    requisicao = requests.get(url)
    try:
        letras.append(requisicao.json()["mus"][0])
    except requests.exceptions.JSONDecodeError:
        time.sleep(4)
        requisicao = requests.get(url)
        print("RESTART")
        print(requisicao)
        letras.append(requisicao.json()["mus"][0])
    else:
        print(requisicao)

for letra in letras :
    chaves = aux.encontra_key(letra["name"], dicionario )

    if chaves is not None :
        dicionario[chaves[0]][chaves[1]][letra["name"].upper()]["letra"] = letra["text"]

with open('data.json', 'w', encoding='utf-8') as fp:
    json.dump(dicionario, fp)
