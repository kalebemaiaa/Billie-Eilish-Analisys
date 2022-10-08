# Billie Eillish 

Neste trabalho reunimos dados da cantora Billie Eilish, seu album, músicas do album, letras, duração e rank, tudo tirado da plataforma Deezer e Vagalume, através de suas API's. Além disso, respondemos perguntas sobre algumas caracteristicas de sua discografia e plotamos gráficos de algumas perguntas dadas, utilizando a biblioteca Seaborn, juntamente com Matplotlib, e a biblioteca WordCloud. 

## Explicação

Há 3 arquivos principais, sendo eles, o arquivo main.py, auxiliar.py e import_data.py. Para utilizar as funções desenvolvidas, deve-se começar realizando o comando 

```pip install -r requirements.txt```.

### Importação dos dados

Para importar os dados necessários para responder as perguntas propostas, utiliza-se o arquivo import_data.py. Este arquivo, resumidamente, utiliza os dados de id do artista, no Deezer e na plataforma Vagalume, para acessar informações sobre a discografia do artista e salva-las em um arquivo .csv, futuramente convertido em dataframe. 

### Perguntas 

Para responder as perguntas, propõe-se no arquivo main.py um exemplo de como utilizar as fuções desenvolvidas para gerar dataframes que colaboram na extração de informações do dados adquiridos.

### Visualização (Gráficos e TagCloud)
  
  Ainda no arquivo main.py, há um exemplo das funções desenvolvidas para plotar, essencialmente, a visualização gráfica que correspende as resposta obtidas.
  
## Documentação

A documentação e explicação de cada função está no arquivo 'documentacao.pdf'.
