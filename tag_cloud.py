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

resposta_2_4 = aux.count_words(df_musicas).to_dict()

lista = []

for palavra,quantity in resposta_2_4.items():
    COUNT = 0
    while COUNT < quantity:
        lista.append(palavra)
        COUNT += 1


TEXT = " ".join(lista)

d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()


BE = np.array(Image.open(os.path.join(d, "./img/be.jpeg")))
WC = WordCloud(background_color="white", max_words=1000, mask=BE, max_font_size=60, collocations = False)

WC.generate(TEXT)

plt.imshow(WC, interpolation="bilinear")
plt.axis("off")
plt.show()
