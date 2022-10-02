"""
Arquivo para responder as perguntas
"""

import pandas as pd
import auxiliar as aux

df_musicas = pd.read_csv("dados_musicas.csv")
df_letras = pd.read_csv("dados_letras.csv")

# Pergunta 1
# mais_ouvidas
indice = df_musicas.groupby(["album"])["rank"].transform(
    max) == df_musicas["rank"]
# menos_ouvidas
indice = df_musicas.groupby(["album"])["rank"].transform(
    min) == df_musicas["rank"]
# Pergunta 2
# longas
indice = df_musicas.groupby(["album"])["duracao"].transform(
    max) == df_musicas["duracao"]
# curtas
indice = df_musicas.groupby(["album"])["duracao"].transform(
    min) == df_musicas["duracao"]

# Pergunta 3
# mais_ouvida
indice = df_musicas.index == df_musicas["rank"].idxmax()
# menos_ouvida
indice = df_musicas.index == df_musicas["rank"].idxmin()

# Pergunta 4
# mais_longa
indice = df_musicas.index == df_musicas["duracao"].idxmax()
# menos_ouvida\
indice = df_musicas.index == df_musicas["duracao"].idxmin()

# Pergunta 5

lista_albuns_premiados = ["Happier Than Ever", "When We All Fall Asleep, Where Do We Go?"]
lista_numero_premiacoes = [[1],[8]]
df_p5 = pd.DataFrame(lista_numero_premiacoes, index=lista_albuns_premiados)

# Pergunta 6
ordenando_rank_duracao = df_musicas.sort_values(
    ["rank", "duracao"])[["nome", "rank", "duracao"]]

# GRUPO 2
# Pergunta 1
lista = []
for titulo in df_musicas["album"].unique():
    titulo = aux.remove_parenteses(titulo)
    palavras = titulo.split()
    for palavra in palavras:
        lista.append(palavra)

contagem = pd.Series(lista).value_counts()

# Pergunta 2
lista = []
for titulo_musica in df_musicas["nome"]:
    titulo_musica = aux.remove_parenteses(titulo_musica)
    for palavra in titulo_musica.split():
        lista.append(palavra)

contagem = pd.Series(lista).value_counts()

# Pergunta 3
lista_albuns = df_musicas["album"].unique()
masks = []
for album in lista_albuns:
    idx = df_musicas["album"] == album
    masks.append(idx)

for idx in masks:
    lista = []
    for nome in df_musicas[idx]["nome"]:
        mask = df_letras["nome"] == nome
        for letra in df_letras[mask]["letra"]:
            letra = aux.limpa_texto(letra)
            for palavra in letra.split():
                lista.append(palavra)

    contagem = pd.Series(lista, dtype=object).value_counts()
    print(contagem)


# Pergunta 4
lista = []
for letra in df_letras["letra"]:
    letra = aux.limpa_texto(letra)
    for palavra in letra.split():
        lista.append(palavra)

contagem = pd.Series(lista).value_counts()

# Pergunta 5




# Pergunta 6



#Grupo 3

#Álbum com mais duracao de musica




#Álbum




#Álbum
