"""
Arquivo para responder as perguntas
"""
import pandas as pd
import auxiliar as aux

df_musicas = pd.read_csv("dados_musicas.csv")
df_musicas.drop(['Unnamed: 0'], axis = 1, inplace=True)

# Pergunta 1
#print(aux.lista_rank(df_musicas, "duracao", True ))

# Pergunta 2
#print(aux.lista_rank(df_musicas, "rank", True ))

# Pergunta 3
#print(aux.lista_rank(df_musicas, "duracao", True,False))

# Pergunta 4
#print(aux.lista_rank(df_musicas, "rank", True, False))

# Pergunta 5

lista_albuns_premiados = ["Happier Than Ever", "When We All Fall Asleep, Where Do We Go?"]
lista_numero_premiacoes = [1,8]
df_p5 = pd.DataFrame(lista_numero_premiacoes, index=lista_albuns_premiados)

# Pergunta 6
ordenando_rank_duracao = df_musicas.sort_values(["rank", "duracao"])[["nome", "rank", "duracao"]]

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
#print(aux.recorrencia_titulos_albuns(df_musicas))

# Pergunta 6
#print(aux.recorrencia_titulos_musicas(df_musicas))

#Grupo 3
# Duracao media das musicas em toda discografia e por album
#print(aux.duracao_media(df_musicas))

# Media de palavras por minuto em toda discografia
#print(aux.palavras_por_minuto(df_musicas))

# Media de palavras por minuto por album
#print(aux.palavras_por_minuto(df_musicas, True))

# Visualizacao
# Seaborn
#aux.plotar_graficos(df_musicas,1)
#aux.plotar_graficos(df_musicas,2)
#aux.plotar_graficos(df_musicas,3)
#aux.plotar_graficos(df_musicas,4)
#aux.plotar_graficos(df_musicas,5)
#aux.plotar_graficos(df_musicas,6)


# Tag Cloud
#aux.tag_clouds(df_musicas, 1, "img/be.jpeg")
#aux.tag_clouds(df_musicas, 2, "img/mic.jpg")
#aux.tag_clouds(df_musicas, 3, "img/nota.jpg")
#aux.tag_clouds(df_musicas,4, "img/billie.png")
