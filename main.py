import pandas as pd
import auxiliar as aux
import json

f = open("data.json")

dados = json.load(f)

dt_musicas = pd.DataFrame(dados["musicas"])
dt_albuns = pd.DataFrame(dados["albuns"])
dt_letras = pd.DataFrame(dados["letras"])

#RESPOSTA PALAVRAS FREQUENTES TITULOS ALBUNS
titulos_albuns = dt_albuns["desc"]
base = pd.Series([],dtype=object)

for titulo in titulos_albuns:
    titulo = aux.tira_parenteses(titulo)
    titulo = titulo.replace("EP","")
    palavras_contadas = aux.conta_valor(titulo)

    base = pd.concat([base,palavras_contadas])

#print(base.value_counts())
#-----------------------------------------------


#RESPOSTA PALAVRAS FREQUENTES TITULOS DAS MUSICAS
titulos_musicas = dt_letras["name"]

base = pd.Series([],dtype=object)

for titulo in titulos_musicas:
    titulo = aux.tira_parenteses(titulo)
    palavras_contadas = aux.conta_valor(titulo)
    base = pd.concat([base, palavras_contadas])

#print(base.value_counts())
#-------------------------------------------
print(dt_musicas)

#RESPOSTA PALAVRAS MAIS COMUNS NAS MUSICAS POR ALBUM

#--------------------------------------------------

#RESPOSTA PALAVRAS MAIS COMUNS NAS MUSICAS EM TODA DISCOGRAFIA
todas_letras = dt_letras["text"]
base = pd.Series([], dtype=object)

for letra in todas_letras:
    palavras_contadas = aux.conta_valor(letra, True)
    base = pd.concat([base,palavras_contadas])

#print(base.value_counts())
#--------------------------------------------------------------
f.close()