from calendar import c
import pandas as pd

def limpa_text(texto: str, parenteses = False)-> str:
    #print(texto)
    texto_limpo = texto.translate({ord(c): " " for c in '"!,?*&%$#@\\/.-'})
    if parenteses is True:
        texto_limpo = texto_limpo.translate({ord(c): " " for c in '()'})
        
    return texto_limpo.upper()

def tira_parenteses(texto: str)-> str:
    if '(' in texto and ')' in texto:
        primeira_fatia = texto.split("(")
        segunda_fatia = texto.split(")")

        return primeira_fatia[0]+ segunda_fatia[1]
    return texto

def conta_valor(texto: str,parenteses=False):
    texto = limpa_text(texto,parenteses)    
    palavras = texto.split()
    return pd.Series(palavras, dtype=object)