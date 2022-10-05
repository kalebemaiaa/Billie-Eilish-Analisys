"""
 Arquivo para visualizar os Gráficos
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

df_musicas = pd.read_csv("dados_musicas.csv")


def plotar_graficos(eixoy,eixox,texto):

    """
    Parametros
    ----------
    eixoy : É o parametro no qual estará na forma string, onde nele dirá qual dado do
            df_musicas será o eixo y no gráfico plotado

    eixox : É o parametro no qual estará na forma string, onde nele dirá qual dado do
             df_musicas será o eixo x no gráfico plotado

    texto : É onde ficará o titulo do gráfico
    
    Raises
    ------
    KeyError
        Erro gerado quando o argumento fornecido não está no dataframe df_músicas

    Return
    -------
        Retorna um gráfico com os eixos conhecidos

    """

    try:
        sns.set_theme()
        fig, ax = plt.subplots(figsize=(7, 3))
        sns.barplot(df_musicas , y = df_musicas[eixoy], x = df_musicas[eixox], ax=ax)
        ax.set_title(texto)
        ax.figure.set_size_inches(12,12)
    except KeyError:
        print("Passe um argumento válido")
    else:
        plt.show()
    return


#Plot pergunta 1 - grafico do rank das musicas por album

plotar_graficos("album","rank", "Gráfico do rank das músicas por álbum ( na base 10^6 )")

# Plot pergunta 2 - Duracao musicas por album

plotar_graficos("album","duracao", "Gráfico da duração das músicas por álbum")

#Plot pergunta 3 - grafico do rank das musicas total

plotar_graficos("nome","rank", "Gráfico do rank de todas as músicas ( na base 10^6 )")

# Plot pergunta 4 - Duracao musicas total

plotar_graficos("nome","duracao", "Gráfico da duração de todas as músicas")

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
