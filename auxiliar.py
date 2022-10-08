# -*- coding: utf-8 -*-
"""
Arquivo auxiliar com funcoes utilizadas para responder as perguntas.
"""
from time import sleep
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import requests

def limpa_texto(texto: str) -> str:
    """
    Parameters
    ----------
    texto : str
        Recebe um texto no formato string como argumento para ser limpo.

    Returns
    -------
    str
        Retorna o texto limpo. Caso o argumento recebido nao seja do tipo string, retorna None.
    """
    lista = []
    if not isinstance(texto, str):
        return
    texto = texto.replace("\\n", " ")
    for palavra in texto:
        palavra = "".join(
            ["" if x in "?!@#$%¨&*-?\\/|;.,1234567890[]()\"~'^" else x.upper() for x in palavra])
        lista.append(palavra)
    return "".join(lista)


def remove_parenteses(texto: str) -> str:
    """
    Parameters
    ----------
    texto : str
        Recebe um texto como argumento.

    Returns
    -------
    str
        Retorna o texto sem os ultimos parenteses e o conteudo dentro dele.

    """
    palavras = texto.split()
    begin, end = None, None
    for i in range(len(palavras)):
        if "(" in palavras[i]:
            begin = i
        if ")" in palavras[i]:
            end = i

    if begin is None or end is None:
        return " ".join(palavras)

    return " ".join(palavras[:begin] + palavras[end + 1:])


def lista_rank(dataframe: pd.DataFrame, atributo: str, condition: bool, in_album: bool = True) -> pd.Series:
    """
    Parametros
    ----------
    dataframe : pd.DataFrame
        Recebe um argumento do tipo Dataframe que deve possuir como colunas as chaves:rank e duracao
    atributo : str
        O atributo se refere a uma coluna do Dataframe
    condition : bool
        Uma variavel booleana obrigatória que deve ser passada para procurar o valor min o max.
        True significa valor maximo e False o valor minimo.
    in_album : bool, optional
        Variavel booleana que refere-se ao escopo onde procurar as mais ouvidas. 
        O valor padrao é True.

    Raises
    ------
    TypeError
        Erro gerado quando o argumento fornecido não é do tipo Dataframe

    Returns
    -------
    TYPE
        Retorna um dataframe com algumas informacoes

    """
    if type(dataframe) != pd.DataFrame:
        raise TypeError(
            "O valor fornecido como argumento 'dataframe' deve ser do tipo Dataframe!")

    if type(condition) != bool:
        raise TypeError(
            "O valor fornecido como argumento 'condition' deve ser do tipo Booleano!")

    if type(atributo) != str:
        raise TypeError(
            "O valor fornecido como argumento 'atributo' deve ser do tipo str!")

    if atributo not in dataframe.keys():
        raise ValueError(
            "O valor fornecido como argumento 'atributo' nao e uma chave para o dataframe")

    if condition == True:
        if in_album == False:
            try:
                index = dataframe.index == dataframe[atributo].idxmax()
            except TypeError:
                print(
                    "O valor fornecido como argumento 'atributo' nao e de um tipo valido!\nOs tipos validos sao: duracao e rank.")
                return
            else:
                return dataframe[index]

        musicas_album = dataframe.groupby(["album"])
        mais_ouvidas_album = musicas_album[atributo].transform(
            max) == dataframe[atributo]

        return dataframe[mais_ouvidas_album]

    if in_album == False:
        try:
            index = dataframe.index == dataframe[atributo].idxmin()
        except TypeError:
            print("O valor fornecido como argumento 'atributo' nao e de um tipo valido!\nOs tipos validos sao: duracao e rank. ")
            return
        else:
            return dataframe[index]

    musicas_album = dataframe.groupby(["album"])
    mais_ouvidas_album = musicas_album[atributo].transform(
        min) == dataframe[atributo]

    return dataframe[mais_ouvidas_album]


def map_text(texto: str) -> dict:
    """
    Parameters
    ----------
    texto : str
        Recebe um texto como argumento.

    Returns
    -------
    dict
        Retorna um dicionário com a contagem das palavras do texto.

    """
    if type(texto) != str:
        raise TypeError("O argumento inserido nao e do tipo string!")
        
    texto = limpa_texto(texto)
    dicionario = {}
    for word in texto.split():
        try:
            dicionario[word] += 1
        except KeyError:
            dicionario[word] = 1

    return dicionario

def concat_sum_dict(dicionario_1, dicionario_2):
    """
    Parameters
    ----------
    dicionario_1 : dict
        Argumento do tipo dicionario com values int.
    dicionario_2 : dict
        Argumento do tipo dicionario com values int.

    Returns
    -------
    dicionario_2 : dict
        Retorna o dicionario concatenado.

    """
    for chave, valor in dicionario_1.items():
        try:
            dicionario_2[chave] += valor
        except KeyError:
            dicionario_2[chave] = valor
        except TypeError:
            print("O tipo do valor inserido nao e inteiro")
            return
    return dicionario_2

def count_words_album(nome_album:str, dataframe: pd.DataFrame) -> pd.Series:
    """
    

    Parameters
    ----------
    nome_album : str
        Nome do album para procurar as musicas.
    dataframe : pd.DataFrame
        Argumento do tipo Dataframe que deve possuir as colunas 'letras' e 'album'.

    Raises
    ------
    TypeError
        Erro gerado caso o argumento inserido nao seja do tipo esperado.
    KeyError
        Erro gerado caso o album inserido nao seja um dos albuns dentro do dataframe.

    Returns
    -------
    TYPE
        Retorna uma serie que mostra a palavra e quantas vezes ela aparece.

    """
    if type(nome_album) != str:
        raise TypeError("O argumento inserido como nome de album nao e do tipo strin!")
        
    if type(dataframe) != pd.DataFrame:
        raise TypeError("O argumento fornecido como dataframe nao e do tipo Dataframe")
    
    if nome_album not in dataframe["album"].values:
        raise KeyError("O argumento inserido como algum nao esta listado como value dos albuns do dataframe")
    
    base = {}
    
    try:
        for letra in dataframe[dataframe["album"] == nome_album]["letras"]:
            if type(letra) == float:
                continue
            dados = map_text(letra)
            base = concat_sum_dict(dados, base)
    
    except KeyError as ke:
        print("O Dataframe nao possui a chave esperada:", ke)
    
    else:
        return pd.Series(base, dtype=object).sort_values(ascending=False)


def count_word_title(lista_titulos) -> dict:
    """
    

    Parameters
    ----------
    lista_titulos : iteravel
        Lista com titulos pela qual iterar.

    Raises
    ------
    TypeError
        Erro gerado caso o argumento nao seja de um tipo interavel.

    Returns
    -------
    dict
        Retorna um dicionario que conta as palavras e o numero de vezes que aparecem.

    """
    if not hasattr(lista_titulos, '__iter__'):
        raise TypeError("o argumento fornecido nao e um tipo iteravel")
    
    base_dentro = {}
    
    for titulo in lista_titulos:
        titulo = remove_parenteses(titulo)
        titulo = limpa_texto(titulo)
        dados = map_text(titulo)
        base_dentro = concat_sum_dict(dados, base_dentro)
        
    return base_dentro

def count_words(dataframe: pd.DataFrame, argumento=None)-> pd.DataFrame:
    """
    Parameters
    ----------
    dataframe : pd.DataFrame
        Recebe um dataframe, onde e esperado ao menos um dos seguintes atributos: 'album', 'letras' ou 'nome'.
    argumento : TYPE, optional
        O valor inserido como argumento e usado para consulta. Possui 4 opcoes, sendo elas:
            1- album: Ve as palavras que mais aparecem nos titulos dos albuns;
            2- nome: Ve as palavras que mais aparecem nos titulos das musicas;
            3- letra: Ve as palavras que mais aparecem nas letras, por album;
            4- None (valor padrao): Ve as palavras que mais aparecem nas letras em toda discografia.

    Raises
    ------
    TypeError
        Erro gerado caso o tipo do argumento inserido como dataframe nao seja Dataframe.
    ValueError
        Erro gerado caso o atributo inserido nao seja do tipo esperado.

    Returns
    -------
    pd.DataFrame
        Retorna um dataframe que mostra a palavra e o numero de vezes que ela aparece.

    """
    if type(dataframe) != pd.DataFrame:
        raise TypeError("O argumento inserido como dataframe nao e do tipo Dataframe!")
    
    base = {}
    
    if argumento is None:
        try:
            for texto in dataframe["letras"]:
                if type(texto) == float:
                    continue
                dados = map_text(texto)
                base = concat_sum_dict(dados, base)
        except KeyError:
            print("O Dataframe inserido nao possui o atributo 'letras'.")
            return 
        
        else:
            return pd.DataFrame(base.values() ,base.keys(), columns = ["Frequencia"])

    elif argumento.upper() == "ALBUM":
        try:
            lista_titulos_albuns = dataframe["album"].unique()
            base = count_word_title(lista_titulos_albuns)
        
        except KeyError:
            print("O Dataframe inserido nao possui o atributo 'album'.")
            return
        
        else:
            return pd.DataFrame(base.values() ,base.keys(), columns = ["Frequencia"])
    
    elif argumento.upper() == "NOME":
        try:
            lista_titulos_musicas = dataframe["nome"]
            base = count_word_title(lista_titulos_musicas)
        except KeyError:
            print("O Dataframe inserido nao possui o atributo 'nome'.")
        
        else:
            return pd.DataFrame(base.values() ,base.keys(), columns = ["Frequencia"])

    elif argumento.upper() == "LETRA":
        try:
            
            lista_albuns = dataframe["album"].unique()
            for album in lista_albuns:
                base[album] = count_words_album(album, dataframe)
        except KeyError:
            print("O Dataframe inserido nao possui o atributo 'album'")
            return
        else:
            return pd.DataFrame(base).fillna(0)
    
    raise ValueError("O parametro inserido como argumento nao é o esperado")

def recorrencia_titulos_albuns(dtframe: pd.DataFrame)-> pd.DataFrame:
    """
    

    Parameters
    ----------
    dtframe : pd.DataFrame
        Um argumento do tipo Dataframe com atributos 'album' e 'letras'.

    Raises
    ------
    TypeError
        Erro gerado caso o argumento passado nao seja do tipo Dataframe.
    ValueError
        Erro gerado caso nao exista ao menos algum dos atributos esperados.

    Returns
    -------
    Dataframe
        Retorna um dataframe que mostra quantas vezes as paravas do titulo aparecem naquele album.

    """
    if type(dtframe) != pd.DataFrame:
        raise TypeError("O argumento inserido nao e do tipo Dataframe")
    
    if not "album" in dtframe.columns or not "letras" in dtframe.columns:
        raise ValueError("O dataframe inserido nao possui a coluna 'album' ou a coluna 'letras'")
    
    lista_titulo_albuns = dtframe["album"].unique()
    titulos_albuns_limpos = [limpa_texto(remove_parenteses(x)) for x in lista_titulo_albuns]
    lista_palavras = [x.split() for x in titulos_albuns_limpos]
    
    base = {}
    for i in range(len(lista_palavras)):
        letras_album = dtframe[dtframe["album"] == lista_titulo_albuns[i]]["letras"].to_list()
        dicionario = {}
        
        for palavra in lista_palavras[i]:
            dicionario[palavra] = 0
            
        for letra in letras_album:
            if type(letra) == float or pd.isna(letra): 
                continue
            
            letra = limpa_texto(letra)
            for palavra in letra.split():
                try:
                    dicionario[palavra] += 1
                except KeyError:
                    continue
         
        base[lista_titulo_albuns[i]] = dicionario
    
    return pd.DataFrame(base).fillna("-")


def recorrencia_titulos_musicas(dtframe: pd.DataFrame) -> pd.DataFrame:
    """
    
    Parameters
    ----------
    dtframe : pd.DataFrame
        Recebe um dataframe com atributos 'nome' e 'letras'.

    Raises
    ------
    TypeError
        Erro gerado caso o argumento inserido nao seja do tipo Dataframe.
    ValueError
        Erro gerado caso o Dataframe nao possua as colunas esperadas.

    Returns
    -------
    pd.DataFrame
        Retorna um dataframe que mostra a quantidade de vezes que o titulo da musica aparece na musica.

    """
    if type(dtframe) != pd.DataFrame:
        raise TypeError("O argumento inserido nao e do tipo Dataframe")
    
    if not "nome" in dtframe.columns or not "letras" in dtframe.columns:
        raise ValueError("O dataframe inserido nao possui a coluna 'nome' ou a coluna 'letras'")
    
    lista_titulos_musicas = dtframe["nome"].to_list()
    
    dicionario = {}
    
    for musica in lista_titulos_musicas:
        letra = dtframe[dtframe["nome"] == musica]["letras"].drop_duplicates()
        letra = str(letra.values)
        letra = limpa_texto(letra)
        
        dicionario_musica = {}
        
        titulo_limpo = limpa_texto(remove_parenteses(musica))
        for palavra in titulo_limpo.split():
            dicionario_musica[palavra] = 0
        
        for palavra in letra.split():
            try:
                dicionario_musica[palavra] += 1
            except KeyError:
                continue

        dicionario[musica] = dicionario_musica

    return pd.DataFrame(dicionario).fillna("-")

def plota_words(resposta, imgPath:str, title:str = None):
    """
    
    Parameters
    ----------
    resposta : pd.DataFrame or pd.Series
        O dataframe ou serie passada servira como base de daos para a plotagem da tag cloud.
    imgPath : TYPE
        O caminho para a imagem escolhida.
    title : TYPE, optional
        Titulo para a figura. The default is None.

    Returns
    -------
    None.

    """
    if type(imgPath) != str:
        raise TypeError("O valor passado como caminho da imagem nao e do tipo str")
        
    lista = []
    for i in range(resposta.size):
        COUNT = 0
        
        while COUNT < resposta.values[i]:
            lista.append(resposta.index[i])
            COUNT += 1
        

    TEXT = " ".join(lista)

    try:
        img = np.array(Image.open(imgPath))
        
    except FileNotFoundError:
        print("Nao foi possivel abrir nenhum arquivo atraves do path passado!")
        
    else:
        WC = WordCloud(background_color="#000", 
                       max_words=1000,
                       mask=img, max_font_size=50, 
                       collocations = False, 
                       contour_width=0.2,
                       contour_color = "#F4FAFC",
                       colormap="Set1" )
    
        WC.generate(TEXT)
        
        plt.imshow(WC, interpolation="bilinear")
        plt.axis("off")
        plt.style.use('dark_background')
        plt.title(title) 
        plt.show()

def tag_clouds(dataframe: pd.DataFrame,num_perg: int, imgPath: str) -> None:
    """
    Parâmetros
    ----------
    dataframe: pd.DataFrame
        Recebe como argumento um dataframe que deve conter como colunas ao menos um dos 3 atributos a seguir:
        1- letras
        2- album
        3- nome
    num_perg : float
        Recebe um argumento do tipo float que deve ser o número da pergunta 
    imgPath : str
        Recebe o caminho da imagem no sistema

    Raises
    ------
    TypeError
        Erro gerado quando algum dos argumentos fornecidos não é do tipo especificado 
    ValueError
        Erro gerado caso o valor passado como num_perg nao esteja entre 1 e 4.
    """
    if type(dataframe) != pd.DataFrame:
        raise TypeError("O valor fornecido como argumento 'dataframe' nao e do tipo Dataframe!")

    if type(num_perg) != int:
        raise TypeError("O valor fornecido como argumento 'num_perg' deve ser do tipo int!")

    if type(imgPath) != str:
        raise TypeError("O valor fornecido como argumento 'imgPath' deve ser do tipo str!")
    
    if num_perg not in [1,2,3,4]:
        raise ValueError("o valor fornecido como num_perg deve estar entre 1 e 4!")
    
    if num_perg == 1:
        resposta = count_words(dataframe, "ALBUM")
        titulo = "Palavras nos titulos dos albuns"
        
    elif num_perg == 2:
        resposta = count_words(dataframe, "NOME")
        titulo = "Palavras nos titulos das musicas"
        
    elif num_perg == 3:
        resposta = count_words(dataframe, "LETRA")
        lista_columnas = resposta.columns
        for coluna in lista_columnas:
            try:
                mini_resposta = resposta[coluna]
                
                titulo = f"Palavras nas letras do album: {coluna}"
                plota_words(mini_resposta, imgPath, titulo)
            except ValueError:
                continue
        return
        
    else:   
        resposta = count_words(dataframe)
        titulo = "Palavras nas letras em toda discografia"     
    plota_words(resposta, imgPath, titulo)

def duracao_media(dataframe:pd.DataFrame) -> dict:
    """
    Args:
        dataframe (pd.DataFrame): Argumento do tipo dataframe que deve possuir as colunas 'album' e 'duracao'
    Raises:
        TypeError: erro gerado caso o argumento inserido nao seja do tipo dataframe
        ValueError: erro gerado caso o dataframe nao possua um dos atributos esperados

    Returns:
        dict: _description_
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O argumento inserido nao e do tipo DataFrame!")
    if "album" not in dataframe.columns :
        raise ValueError("O dataframe inserido nao tem o atributo album!")
    if "duracao" not in dataframe.columns :
        raise ValueError("O dataframe inserido nao tem o atributo duracao!")

    lista_albuns = dataframe["album"].unique()
    dicionario = {
        "all_discografia": dataframe["duracao"].mean()
    }
    for album in lista_albuns:
        mask = dataframe["album"] == album
        media_album = dataframe[mask]["duracao"].mean()
        dicionario[album] = media_album
    return dicionario

def lista_palavras(serie:pd.Series) -> list:
    """

    Args:
        serie (pd.Series): Serie que contenha as letras.

    Raises:
        TypeError: erro gerado caso o argumento nao seja do tipo Series.

    Returns:
        list: retorna uma lista com todas as palavras da letra.
    """
    if not isinstance(serie, pd.Series):
        raise TypeError("O argumento inserido nao e do tipo Series")
    words_list = []
    for letra in serie:
        letra = limpa_texto(letra)

        if letra is None:
            continue
        for palavra in letra.split():
            words_list.append(palavra)
    return words_list

def palavras_por_minuto(dataframe:pd.DataFrame, in_album = False):
    """

    Args:
        dataframe (pd.DataFrame): Argumento que deve possuir, ao menos, as colunas 'letras' e 'duracao'
        in_album (bool, optional): Argumento que avaliar o escopo do funcao. Se for True, avaliara a quantidade de palavras por minuto em cada album. Se for False, avaliara a quantidade de palavras por minuto em toda discografia. Defaults to False.

    Raises:
        TypeError: Erro gerado caso algum dos argumentos inseridos nao seja do tipo esperado.
        ValueError: Erro gerado caso o dataframe nao possua alguma das colunas esperadas.

    Returns:
        float or dict: retorna um numero com ponto flutuante ou um dicionario com nome de albuns com key e numeros de ponto flutuante como values.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O argumento inserido como dataframe nao e do tipo Dataframe!")
    if not isinstance(in_album, bool):
        raise TypeError("O argumento inserido como in_album nao e do tipo booleano!")
    if "letras" not in dataframe.columns:
        raise ValueError("O dataframe passado nao possui 'letras' como coluna.")
    if "duracao" not in dataframe.columns:
        raise ValueError("O dataframe passado nao possui 'duracao' como coluna.")
    if in_album is False:
        total_palavras = len(lista_palavras(dataframe["letras"]))
        total_minutos = dataframe["duracao"].sum() / 60
        return total_palavras / total_minutos

    dicionario = {}
    lista_albuns = dataframe["album"].unique()

    for album in lista_albuns:
        mask = dataframe["album"] == album
        total_palavras = len(lista_palavras(dataframe[mask]["letras"]))
        duracao_album = dataframe[mask]["duracao"].sum() / 60
        dicionario[album] = total_palavras / duracao_album
    return dicionario

def plotar_graficos(dataframe:pd.DataFrame, num_perg:int)-> None:
    """

    Args:
        dataframe (pd.DataFrame): dataframe onde se espera algumas colunas 
        num_perg (int): o numero da pergunta do grupo 1. E um inteiro entre 1 e 6

    Raises:
        TypeError: erro gerado caso o argumento dataframe nao seja do tipo Dataframe ou o argumento num_perg nao seja do tipo int
        ValueError: erro gerado caso o argumento num_perg nao esteja dentro do intervalo desejado

    Returns:
        None: Plota um grafico 
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O argumento inserido como dataframe nao e do tipo dataframe")
        
    if not isinstance(num_perg, int):
        raise TypeError("O argumento inserido como num_per nao e do tipo inteiro")

    if num_perg not in [1,2,3,4,5,6]:
        raise ValueError("O argumento fornecido como num_perg deve ser do tipo int.")

    eixoy, eixox = None, None

    if num_perg == 1:
        eixox, eixoy = "rank", "album"
        titulo = ""
    elif num_perg == 2:
        eixox, eixoy = "duracao", "album"
        titulo = ""
    elif num_perg == 3:
        eixox, eixoy = "rank", "nome"
        titulo = ""
    elif num_perg == 4:
        eixox, eixoy = "duracao", "nome"
        titulo = ""
    elif num_perg == 5:
        lista_albuns_premiados = ["Happier Than Ever", "When We All 'Fall Asleep, Where Do We Go?"]
        lista_numero_premiacoes = [1,8]
        sns.barplot(y = lista_numero_premiacoes, x = lista_albuns_premiados, width=0.2)
        plt.title("Albuns Premiados")
        return plt.show()
    else:
        eixox, eixoy = "duracao", "nome"
        plt.scatter(dataframe["duracao"], dataframe["rank"])
        plt.title("Relação entre a duração e popularidade de uma música")
        return plt.show()

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(figsize=(7, 3))
    try:
        sns.barplot(dataframe , y = dataframe[eixoy], x = dataframe[eixox], ax=ax, width=0.3)
        ax.set_title(titulo)
        ax.figure.set_size_inches(12,12)
    except KeyError as ke:
        print("O dataframe inserido nao possui os atributos esperados!\n\t",ke)
    else:
        plt.show()

def get_data_deezer(artist_id:str)->pd.DataFrame:
    """
    Parameters
    ----------
    artist_id : str
        O id do artista na plataforma do Deezer.

    Returns
    -------
    DataFrame
        Retorna um dataframe com as informa��es sobre a musica.

    """
    if not isinstance(artist_id, str):
        raise TypeError("O atributo fornecido nao e do tipo str")
    url_artista = f"https://api.deezer.com/artist/{artist_id}"
    dados_artista = requests.get(url_artista)
    dados_tracklist = requests.get(dados_artista.json()["tracklist"])
    musicas_data = dados_tracklist.json()["data"]
    estrutura_musicas = [{
        "album": music["album"]["title"].upper(),
        "duracao": music["duration"],
        "rank": music["rank"],
        "nome": music["title"].upper()} for music in musicas_data]

    return pd.DataFrame(estrutura_musicas)

def get_data_vagalume(chave_api:str, artista_name:str)->pd.DataFrame:
    """
    Parameters
    ----------
    chave_api : str
        A key dada ao acessar a api do site vagalume.
    artista_name : str
        Nome do artista procurado.

    Returns
    -------
    DataFrame
        Retorna um dataframe com os nomes das musicas e as suas respectibas letras.

    """
    url_artista = f"https://www.vagalume.com.br/{artista_name}/index.js"
    requisicao_artista_json = requests.get(url_artista).json()
    music_data = [id_m for id_m in requisicao_artista_json["artist"]["lyrics"]["item"]]
    letras = []
    for musica in music_data:
        id_musica = musica["id"]
        url_music = f"https://api.vagalume.com.br/search.php?musid={id_musica}&apikey={chave_api}"
        requisicao_musica = requests.get(url_music)
        try:
            letras.append({
                "letra": requisicao_musica.json()["mus"][0]["text"].upper(),
                "nome": requisicao_musica.json()["mus"][0]["name"].upper()
                })
        except ValueError:
            print("restart too many requests, codigo:\t", requisicao_musica)
            sleep(4)
            requisicao_musica = requests.get(url_music)
            letras.append({
                "letra": requisicao_musica.json()["mus"][0]["text"].upper(),
                "nome": requisicao_musica.json()["mus"][0]["name"].upper()
                })
        else:
            print(requisicao_musica)

    return  pd.DataFrame(letras)

def get_letras(dataframe_musicas:pd.DataFrame, dataframe_letras:pd.DataFrame)->list:
    """
    Parameters
    ----------
    dataframe_musicas : pd.DataFrame
        Um dataframe que deve contar o nome da musica como uma coluna.
    dataframe_letras : pd.DataFrame
        Um dataframe que deve contar o nome da musica e suas letras.

    Returns
    -------
    list
        A funcao devolve uma lista que para cada nome em um dataframe associa a letra dessa musica
        ou o valor None.

    """
    if not isinstance(dataframe_musicas, pd.DataFrame) or not isinstance(dataframe_letras, pd.DataFrame):
        raise TypeError("O argumento fornecido nao e do tipo dataframe")
    if "nome" not in dataframe_musicas.columns:
        raise ValueError("O dataframe nao possui a coluna nome")
    if "nome" not in dataframe_letras.columns:
        raise ValueError("O dataframe nao possui a coluna letras")
    lista = []
    for music_name in dataframe_musicas["nome"]:
        info = dataframe_letras[dataframe_letras["nome"]==music_name]["letra"].values
        if len(info) == 1:
            lista.append(info)
        else:
            lista.append(None)
    return lista