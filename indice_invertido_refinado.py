# -*- coding: UTF-8 -*-
# encoding: iso-8859-1
# encoding: win-1252

import string
import re

from collections import Counter

#metodo que le o arquivo wikipedia
def leWiki():
    arq = open('oi.txt', 'r')
    texto = arq.read()
    arq.close()
    return texto.lower()
    
#metodo para retirar os caracteres indesejados do arquivo
def cleanText(arquivo):    
    arquivo = re.sub(r"&.{2,4};"," ", arquivo)
    arquivo = re.sub(r"\\{\\{!\\}\\}", " ", arquivo)
    arquivo = arquivo.replace("[[", " ")
    arquivo = arquivo.replace("]]", " ")
    arquivo = re.sub("{{.*?}}", "", arquivo)
    arquivo = re.sub("<.*?>", "", arquivo)
    arquivo = re.sub("[^a-z0-9çáéíóúàãõâêô-]", " ", arquivo)
    arquivo = re.sub(r"\n","", arquivo)	
    return arquivo.split(" ")
    
"""neste metodo eu irei criar primeiramente um dicionario onde as chaves sao os numeros dos documentos e os valores sao as palavras que
compoem esse documento """
def criaDict(texto):
	palavras = texto
	dicionario = {}
	while palavras != '':
		if palavras.find('<docno>') != -1: #percorrer o documento enquanto houver a tag <docno>
			
			posI = palavras.find('<docno>') + 7
			posF = palavras.find('</docno>') 
			
			chave = palavras[posI:posF] #pegando o numero de cada documento, o que esta entre a tag <docno>
			
			posI2 = palavras.find('<headline>') + 10
			posF2 = palavras.find('</headline')
			
			titulo = palavras [posI2:posF2] #pegando o titulo de cada documento, o que esta entre a tag <headline>
			
			dicionario[chave] = [titulo]
			
			posI3 = palavras.find('<p>') + 3
			posF3 = palavras.find('</p>')
			
			conteudo = palavras [posI3:posF3] #pegando o texto de cada documento, o que esta entre a tag <p>
			
			conteudo = cleanText(conteudo) #tirando os caracteres indesejados
			
			for palavra in conteudo:  #o conteudo fica como uma lista de palavras, por isso percorrer essa lista e adicionar ao dicionario
				if palavra != "":	  #tirando os vazios que existem na lista
					dicionario[chave].append(palavra)
				
			
			palavras = palavras[posF3 + 4:] #o conteudo a ser percorrido agora é o que vem depois da tag </p>
			
		else:
			palavras = ''
	
	return dicionario
		
"""Com um dicionario criado a partir dos documentos existentes, irei criar o indice invertido e escreve-lo num arquivo .txt"""
def criaIndiceInvertido(texto):
	dic = criaDict(texto)
	indice_invertido = {}
	indice_refinado = {}
	arq = open("indice_invertido.txt", "w")
	
	
	"""Percorro as chaves e valores do dicionario e vejo se o novo dicionario (indice_invertido) já possui uma determinada chave,
	o seja, verifico se aquela palavra ja eh uma chave do indice invertido. Se ja for, adiciono aquele documento aos seus valores,
	se nao crio uma nova chave no indice_invertido"""
	for k,v in dic.iteritems(): 
		for palavra in v:
			if indice_invertido.has_key(palavra):
				if k not in indice_invertido[palavra]: #verifico se o documento ja esta nos valores de determinada chave e so insiro ele nos valores se não estiver
					indice_invertido[palavra].append(int(k))
			else:
				indice_invertido[palavra] = [int(k)]
	
	
	for termo, docs in indice_invertido.iteritems(): #percorre as palavras e a lista de documentos que elas se encontram 
		idf = len(docs)  #idf eh igual a quantidade de documentos que aquela palavra se encontra
		indice_refinado[termo] = {idf:[]}  #criando um dicionario dentro do outro para guardar as tuplas que irao conter (doc, tf_termo)
		cnt = Counter()  #contador que ira dizer quantas vezes a palavra aparece em determinado doc
		for doc in docs:    #percorrendo os documentos que tem aquela palavra
			cnt.clear()	
			for palavra in dic[str(doc)]:
				cnt[palavra] += 1
				
			tupla = ('doc_'+ str(doc), cnt[termo])
			if tupla not in indice_refinado[termo][idf]: #se o dicionario não tiver a tupla (doc, tf_termo) adiciona
				indice_refinado[termo][idf].append(('doc_'+ str(doc), cnt[termo]))
				
	return indice_refinado
	




def score_BM25(n, f, qf, r, N, dl, avdl):
	K = compute_K(dl, avdl)
	first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
	second = ((k1 + 1) * f) / (K + f)
	third = ((k2+1) * qf) / (k2 + qf)
	return first * second * third


def compute_K(dl, avdl):
	k1 = 1
	k2 = 3
	b = 0
	R = 0.0
	
	return k1 * ((1-b) + b * (float(dl)/float(avdl)) )

print criaIndiceInvertido(leWiki())
