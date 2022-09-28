import json
import requests
import time

key_apy = "a829b6e84397c7592f558d850b888203"
artista = "billie-eilish"

teste = requests.get("https://www.vagalume.com.br/" + artista + "/index.js")

dados = teste.json()

musicas = [x for x in dados["artist"]["lyrics"]["item"]]
albuns = [x for x in dados["artist"]["albums"]["item"]]
letras = []

for song in musicas:
    url = "https://api.vagalume.com.br/search.php?musid=" + song["id"] + "&apikey=" + key_apy
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


dicionario = {
    "musicas": musicas,
    "albuns":albuns, 
    "letras": letras
}
with open('data.json', 'w') as fp:
    json.dump(dicionario, fp)