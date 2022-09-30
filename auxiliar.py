# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:21:15 2022

@author: b47133
"""

def limpa_texto(texto:str)->str:
    lista =[]
    for palavra in texto:
        palavra = "".join(["" if x in '?!@#$%¨&*"?\\/|;.,1234567890' else x.upper() for x in palavra])
        lista.append(palavra)
    return "".join(lista)
    
def remove_parenteses(texto:str)->str:
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