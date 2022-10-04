"""
Arquivo para responder as perguntas
"""

import pandas as pd
import auxiliar as aux

df_musicas = pd.read_csv("dados_musicas.csv")

# Pergunta 1
# print(aux.lista_rank(df_musicas, "duracao", True ))

# Pergunta 2
# print(aux.lista_rank(df_musicas, "rank", True ))

# Pergunta 3
# print(aux.lista_rank(df_musicas, "duracao", True,False))

# Pergunta 4
# print(aux.lista_rank(df_musicas, "rank", True, False))

# Pergunta 5

lista_albuns_premiados = ["Happier Than Ever", "When We All Fall Asleep, Where Do We Go?"]
lista_numero_premiacoes = [[1],[8]]
df_p5 = pd.DataFrame(lista_numero_premiacoes, index=lista_albuns_premiados)

# Pergunta 6
ordenando_rank_duracao = df_musicas.sort_values(
    ["rank", "duracao"])[["nome", "rank", "duracao"]]

# GRUPO 2
# Pergunta 1
#print(aux.count_words(df_musicas, "album"))

# Pergunta 2
#print(aux.count_words(df_musicas, "NOME"))

# Pergunta 3
#print(aux.count_words(df_musicas, "LETRA"))

# Pergunta 4
#print(aux.count_words(df_musicas))

# Pergunta 5




# Pergunta 6





#Grupo 3

# Frequencia de lançamento por ano

indice = df_musicas["duracao"].median()
print(indice)

# Media de beats por minuto de toda discografia


indice = df_musicas["duracao"].var()
print(indice)


# Media de beats por minuto por album

indice = df_musicas["duracao"].std()
print(indice)