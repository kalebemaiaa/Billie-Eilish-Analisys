# -*- coding: utf-8 -*-
"""
Arquivo auxiliar com funcoes utilizadas para responder as perguntas.
"""
import pandas as pd

df_musicas = pd.read_csv("dados_musicas.csv")

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
    if type(texto ) != str:
        print(texto)
        return
    
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
        Recebe um argumento do tipo Dataframe que deve possuir como colunas as chaves: rank e duracao 
    atributo : str
        O atributo se refere a uma coluna do Dataframe
    condition : bool
        Uma variavel booleana obrigatória que deve ser passada para procurar o valor minimo ou maximo.
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
        
    texto = texto.replace("\\n", " ")
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
