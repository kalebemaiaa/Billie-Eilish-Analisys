import pandas as pd
import json

f = open("data.json", encoding="utf-8")

dados = json.load(f)

def encontra_key(nome_musica, data):
    for album in data:
        for i in range(len(data[album])):
            if list(data[album][i].keys())[0] == nome_musica.upper():
                return (album, i)

def limpa_text(texto: str, parenteses = False)-> str:
    texto_limpo = texto.translate({ord(c): " " for c in '"!,?*&%$#@\\/.-'})
    if parenteses is True:
        texto_limpo = texto_limpo.translate({ord(c): " " for c in '()'})
        
    return texto_limpo.upper()

def tira_parenteses(texto: str)-> str:
    if '(' in texto and ')' in texto:
        primeira_fatia = texto.split("(")
        segunda_fatia = texto.split(")")

        return primeira_fatia[0]+ segunda_fatia[1]
    return texto

def rank_ouvidas_por_album(dados):
    index = []
    colunas = ["Mais ouvida", "Menos ouvidas"]
    informacoes = []
    for album in dados:
        index.append(album)
        rank_album = []
        nome_music = []
        for musica in dados[album]:
            for key, values in musica.items():
                rank_album.append(values["rank"])
                nome_music.append(key)

        dados_album = pd.Series(rank_album, nome_music)
        informacoes.append((dados_album.idxmax(), dados_album.idxmin()))

    return pd.DataFrame( informacoes, index=index, columns = colunas)

def duracao_por_album(dados):
    index = []
    colunas = ["Mais Longas", "Menos Curtas"]
    informacoes = []
    for album in dados:
        index.append(album)
        rank_album = []
        nome_music = []
        for musica in dados[album]:
            for key, values in musica.items():
                rank_album.append(values["duracao"])
                nome_music.append(key)

        dados_album = pd.Series(rank_album, nome_music)
        informacoes.append((dados_album.idxmax(), dados_album.idxmin()))

    return pd.DataFrame( informacoes, index=index, columns = colunas)

def rank_ouvidas_historia(dados):
    index = []
    data = []
    for albuns in dados:
        for musicas in dados[albuns]:
            for x,y in musicas.items():
                index.append(x)
                data.append(y["rank"])

    return pd.Series(data, index)

def rank_duracao_historia(dados):
    index = []
    data = []
    for albuns in dados:
        for musicas in dados[albuns]:
            for x,y in musicas.items():
                index.append(x)
                data.append(y["duracao"])

    return pd.Series(data, index)

def palavras_titulos_albuns(dados):
    lista = []
    for album in dados:
        album = tira_parenteses(album)
        album = album.split()
        for word in album:
            lista.append(word)

    return pd.Series(lista).value_counts()

def palavras_titulos_musicas(dados):
    lista = []
    for album in dados:
        for musicas in dados[album]:
            for x,y in musicas.items():
                for k in x.split():
                    k = tira_parenteses(k)
                    lista.append(k)

    return pd.Series(lista).value_counts()

def palavras_musica_album(dados):
    retorno = []
    for album in dados:
        data = []
        for musica in dados[album]:
            for x,y in musica.items():
                try:
                    for palavra in y["letra"].split():
                        data.append(palavra)

                except KeyError:
                    continue
        retorno.append(pd.Series(data, dtype=object).value_counts())

    return retorno
    
def palavras_discografia(dados):
    lista = []
    for album in dados:
        for musicas in dados[album]:
            for x in musicas.values():
                try:
                    for y in x["letra"].split():
                        y = limpa_text(y)
                        lista.append(y)
                except KeyError:
                    continue

    return pd.Series(lista).value_counts()