"""
Visualização de palavras como imagens
"""
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import auxiliar as aux
from wordcloud import WordCloud

df_musicas = pd.read_csv("dados_musicas.csv")

def tag_clouds(num_perg: float, imgPath: str):
    """
    Parâmetros
    ----------
    num_perg : float
        Recebe um argumento do tipo float que deve ser o número da pergunta 
    imgPath : str
        Recebe ocaminho da imagem no sistema

    Raises
    ------
    TypeError
        Erro gerado quando algum dos argumentos fornecidos não é do tipo especificado 
    """
    if type(num_perg) != float:
        raise TypeError("O valor fornecido como argumento 'num_perg' deve ser do tipo float")

    if type(imgPath) != str:
        raise TypeError("O valor fornecido como argumento 'imgPath' deve ser do tipo str")

    try:
        if num_perg == 2.1:
            resposta = aux.count_words(df_musicas, "ALBUM").to_dict()
        elif num_perg == 2.2:
            resposta = aux.count_words(df_musicas, "NOME").to_dict()
        elif num_perg == 2.4:    
            resposta = aux.count_words(df_musicas).to_dict() 
            
        lista = []
        for palavra,quantity in resposta.items():
            COUNT = 0
            while COUNT < quantity:
                lista.append(palavra)
                COUNT += 1

        TEXT = " ".join(lista)

        d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

        img = np.array(Image.open(os.path.join(d, imgPath)))
        WC = WordCloud(background_color="white", max_words=1000, mask=img, max_font_size=60, collocations = False)

        WC.generate(TEXT)
        
        plt.imshow(WC, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    except:
        print('Me dê um argumento válido!') 

# Tag Cloud resposta pergurta 1 do grupo de perguntas 2

tag_clouds(2.1, "./img/mic.jpg")

# Tag Cloud resposta pergurta 2 do grupo de perguntas 2

tag_clouds(2.2, "./img/nota.jpg")

# Tag Cloud resposta pergurta 4 do grupo de perguntas 2

tag_clouds(2.4, "./img/be.jpeg")