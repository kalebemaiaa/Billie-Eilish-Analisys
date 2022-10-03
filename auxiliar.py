# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:21:15 2022

@author: b47133
"""
import pandas as pd

df_musicas = pd.read_csv("dados_musicas.csv")


def limpa_texto(texto: str) -> str:
    lista = []
    for palavra in texto:
        palavra = "".join(
            ["" if x in "?!@#$%¨&*-?\\/|;.,1234567890[]()\"'" else x.upper() for x in palavra])
        lista.append(palavra)
    return "".join(lista)


def remove_parenteses(texto: str) -> str:
    palavras = texto.split()
    begin, end = None, None
    for i in range(len(palavras)):
        if "(" in palavras[i]:
            begin = i
        if ")" in palavras[i]:
            end = i

    if begin != None and end != None:
        return " ".join(palavras[:begin] + palavras[end + 1:])

    return " ".join(palavras)


def lista_rank(dataframe: pd.DataFrame, atributo: str, condition: bool, inAlbum: bool = True) -> pd.Series:
    """
    Parametros
    ----------
    dataframe : pd.DataFrame
        Recebe um argumento do tipo Dataframe que deve possuir como colunas as chaves: rank e duracao 
    atributo : str
        O atributo se refere a uma coluna do Dataframe
    condition : bool
        Uma variavel booleana obrigatória que deve ser passada para procurar o valor minimo ou maximo.
        True significa valor maximo e False o valor minimo.
    inAlbum : bool, optional
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
        if inAlbum == False:
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

    if inAlbum == False:
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


def map_text(texto):
    texto = texto.replace("\\n", " ")
    texto = limpa_texto(texto)
    dicionario = {}
    for word in texto.split():
        try:
            dicionario[word] += 1
        except KeyError:
            dicionario[word] = 1

    return dicionario


def count_words_album(nome_album, dataframe):
    basesinha = {}
    for letra in dataframe[dataframe["album"] == nome_album]["letras"]:
        if type(letra) == float:
            continue
        dados = map_text(letra)
        for chave, valor in dados.items():
            try:
                basesinha[chave] += valor
            except KeyError:
                basesinha[chave] = valor
    return pd.Series(basesinha).sort_values(ascending=False)


def count_words(dataframe: pd.DataFrame, argumento=None):
    base = {}

    def to_base(dictionary):
        for chave, valor in dictionary.items():
            try:
                base[chave] += valor
            except KeyError:
                base[chave] = valor

    if argumento == None:
        for texto in dataframe["letras"]:
            if type(texto) == float:
                continue
            dados = map_text(texto)
            to_base(dados)
        return pd.Series(base).sort_values(ascending=False)

    if argumento.upper() == "ALBUM":
        for titulo_album in dataframe["album"].unique():
            titulo_album = remove_parenteses(titulo_album)
            titulo_album = limpa_texto(titulo_album)
            dados = map_text(titulo_album)
            to_base(dados)
        return pd.Series(base).sort_values(ascending=False)
    if argumento.upper() == "NOME":
        for titulo_music in dataframe["nome"]:
            titulo_music = remove_parenteses(titulo_music)
            titulo_music = limpa_texto(titulo_music)
            dados = map_text(titulo_music)
            to_base(dados)
        return pd.Series(base).sort_values(ascending=False)

    if argumento.upper() == "LETRA":
        lista_albuns = dataframe["album"].unique()
        for album in lista_albuns:
            base[album] = count_words_album(album, dataframe)

        return base
