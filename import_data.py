"""
    Este arquivo serve para importar a base da dos utilizada para fazer as analises.
"""
from time import sleep
import requests
import pandas as pd


# API VAGALUME
# LINK: https://www.vagalume.com.br/
KEY_APY_VAGALUME = "a829b6e84397c7592f558d850b888203"
ARTIST_NAME = "billie-eilish"

# API DEEZER
BILLIE_ID_DEEZER = "9635624"

def get_data_deezer(artist_id:str)->pd.DataFrame:
    """
    Parameters
    ----------
    artist_id : str
        O id do artista na plataforma do Deezer.

    Returns
    -------
    DataFrame
        Retorna um dataframe com as informações sobre a musica.

    """
    
    url_artista = f"https://api.deezer.com/artist/{artist_id}"
    dados_artista = requests.get(url_artista)
    dados_tracklist = requests.get(dados_artista.json()["tracklist"])
    musicas_data = dados_tracklist.json()["data"]
    
    estrutura_musicas = [{
        "album": music["album"]["title"].upper(),
        "duracao": music["duration"],
        "rank": music["rank"],
        "nome": music["title"].upper()} 
        for music in musicas_data]

    return pd.DataFrame(estrutura_musicas)

get_data_deezer(BILLIE_ID_DEEZER)

def get_data_vagalume(chave_api:str, artista_name:str)->pd.DataFrame:
    """
    Parameters
    ----------
    chave_api : str
        A key dada ao acessar a api do site vagalume.
    artista_name : str
        Nome do artista procurado.

    Returns
    -------
    DataFrame
        Retorna um dataframe com os nomes das musicas e as suas respectibas letras.

    """
    url_artista = f"https://www.vagalume.com.br/{artista_name}/index.js"
    requisicao_artista_json = requests.get(url_artista).json()
    music_data = [id_m for id_m in requisicao_artista_json["artist"]["lyrics"]["item"]]  
    letras = []
    for musica in music_data:
        id_musica = musica["id"]
        url_music = f"https://api.vagalume.com.br/search.php?musid={id_musica}&apikey={chave_api}"
        requisicao_musica = requests.get(url_music)
        try:
            letras.append({
                "letra": requisicao_musica.json()["mus"][0]["text"].upper(),
                "nome": requisicao_musica.json()["mus"][0]["name"].upper()
                })
        except ValueError:
            print("restart too many requests, codigo:\t", requisicao_musica)
            sleep(4)
            requisicao_musica = requests.get(url_music)
            letras.append({
                "letra": requisicao_musica.json()["mus"][0]["text"].upper(),
                "nome": requisicao_musica.json()["mus"][0]["name"].upper()
                })
        else:
            print(requisicao_musica)

    return  pd.DataFrame(letras)

def get_letras(dataframe_musicas:pd.DataFrame, dataframe_letras:pd.DataFrame)->list:
    """


    Parameters
    ----------
    dataframe_musicas : pd.DataFrame
        Um dataframe que deve contar o nome da musica como uma coluna.
    dataframe_letras : pd.DataFrame
        Um dataframe que deve contar o nome da musica e suas letras.

    Returns
    -------
    list
    
        A função devolve uma lista que para cada nome em um dataframe associa a letra dessa musica ou o valor None.

    """
    lista = []
    
    for music_name in dataframe_musicas["nome"]:
        info = dataframe_letras[dataframe_letras["nome"]==music_name]["letra"].values
        if len(info) == 1:
            lista.append(info)
        else:
            lista.append(None)
    
    return lista


df_musicas = get_data_deezer(BILLIE_ID_DEEZER)
df_letras = get_data_vagalume(KEY_APY_VAGALUME, ARTIST_NAME)
df_musicas = df_musicas.assign(letras=get_letras(df_musicas, df_letras))

df_musicas.to_csv("dados_musicas.csv")
    