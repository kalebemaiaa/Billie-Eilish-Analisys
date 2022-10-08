"""
 Arquivo para visualizar os Gráficos
"""

import matplotlib.pyplot as plt
import pandas as pd

df_musicas = pd.read_csv("dados_musicas.csv")

# Plot pergunta 5 - Albuns premiados

lista_albuns_premiados = ["Happier Than Ever", "When We All 'Fall Asleep, Where Do We Go?"]
lista_numero_premiacoes = [[1],[8]]
df_p5 = pd.DataFrame(lista_numero_premiacoes, index=lista_albuns_premiados)
plt.bar(["Happier Than Ever","When We All 'Fall Asleep, Where Do We Go?"],[1,8], width=0.13)
plt.title("Albuns Premiados")
plt.show()

# plot pergunta 6 - duração e popularidade

plt.scatter(df_musicas["duracao"], df_musicas["rank"])
plt.title(" Relação entre a duração e popularidade de uma música ")
plt.show()
