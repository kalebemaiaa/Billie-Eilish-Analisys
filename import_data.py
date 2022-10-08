"""
    Este arquivo serve para importar a base de dados utilizada para fazer as analises.
"""
import auxiliar as aux
# API VAGALUME
# LINK: https://www.vagalume.com.br/
KEY_APY_VAGALUME = "a829b6e84397c7592f558d850b888203"
ARTIST_NAME = "billie-eilish"

# API DEEZER
BILLIE_ID_DEEZER = "9635624"

df_musicas = aux.get_data_deezer(BILLIE_ID_DEEZER)
df_letras = aux.get_data_vagalume(KEY_APY_VAGALUME, ARTIST_NAME)
df_musicas = df_musicas.assign(letras=aux.get_letras(df_musicas, df_letras))

df_musicas.to_csv("dados_musicas.csv")
