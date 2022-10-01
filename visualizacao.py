import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



df_musicas = pd.read_csv("dados_musicas.csv")
df_letras = pd.read_csv("dados_letras.csv")


#Plot pergunta 1 - grafico do rank das musicas por album

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
df_musicas = pd.read_csv("dados_musicas.csv")

indice = df_musicas.groupby(["rank"])

plt.bar(df_musicas["album"], df_musicas["rank"])
# plt.text(5,4,"AHHHHH")
# plt.show()

# Plot pergunta 2 - Duracao musicas por album


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
df_musicas = pd.read_csv("dados_musicas.csv")

indice = df_musicas.groupby(["duracao"])

plt.bar(df_musicas["album"], df_musicas["duracao"])  
# plt.show()


#Plot pergunta 3 - grafico do rank das musicas total

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
df_musicas = pd.read_csv("dados_musicas.csv")

indice = df_musicas.groupby(["rank"])

plt.bar(df_musicas["nome"], df_musicas["rank"])
# plt.text(5,4,"AHHHHH")
# plt.show()

# Plot pergunta 4 - Duracao musicas total

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
df_musicas = pd.read_csv("dados_musicas.csv")

indice = df_musicas.groupby(["duracao"])

plt.bar(df_musicas["nome"], df_musicas["duracao"])  
# plt.show()

# Plot pergunta 5 - Albuns premiados

lista_albuns_premiados = ["Happier Than Ever", "When We All 'Fall Asleep, Where Do We Go?"]
lista_numero_premiacoes = [[1],[8]]
df_p5 = pd.DataFrame(lista_numero_premiacoes, index=lista_albuns_premiados)
plt.bar(["Happier Than Ever","When We All 'Fall Asleep, Where Do We Go?"],[1,8], width=0.13, edgecolor = "red", linewidth=0.7)
# plt.show()


# plot pergunta 6 - duração e popularidade 

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
df_musicas = pd.read_csv("dados_musicas.csv")

indice = df_musicas.groupby(["rank"])
plt.bar(df_musicas["duracao"], df_musicas["rank"])
#plt.show()




















# sns.relplot(p)
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True
# headers = ['Name', 'Age', 'Marks']
# df = pd.read_csv('dados_musicas.csv', names=headers)
# p.set_index('rank').plot()
