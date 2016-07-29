# -*- coding: UTF-8 -*-
# encoding: iso-8859-1
# encoding: win-1252

import string
import re
import math

from collections import Counter

tamanho_dict = 0
dicionario = {}
indice_invertido = {}
indice_refinado = {}

#metodo que le o arquivo wikipedia
def leWiki(documento):
	arq = open(documento, 'r')
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
		
		tamanho_dict = len(dicionario)
		
	return dicionario
		
"""Com um dicionario criado a partir dos documentos existentes, irei criar o indice invertido e escreve-lo num arquivo .txt"""
def criaIndiceInvertido():

	"""Percorro as chaves e valores do dicionario e vejo se o novo dicionario (indice_invertido) já possui uma determinada chave,
	o seja, verifico se aquela palavra ja eh uma chave do indice invertido. Se ja for, adiciono aquele documento aos seus valores,
	se nao crio uma nova chave no indice_invertido"""
	for k,v in dicionario.iteritems(): 
		for palavra in v:
			if indice_invertido.has_key(palavra):
				if k not in indice_invertido[palavra]: #verifico se o documento ja esta nos valores de determinada chave e so insiro ele nos valores se não estiver
					indice_invertido[palavra].append(int(k))
			else:
				indice_invertido[palavra] = [int(k)]
	
	
	return indice_invertido
	

def criaIndiceRefinado():
	for termo, docs in indice_invertido.iteritems(): #percorre as palavras e a lista de documentos que elas se encontram 
		idf = 1.0/len(set(docs))  #idf eh igual a quantidade de documentos que aquela palavra se encontra
		indice_refinado[termo] = {idf:[]}  #criando um dicionario dentro do outro para guardar as tuplas que irao conter (doc, tf_termo)
		cnt = Counter()  #contador que ira dizer quantas vezes a palavra aparece em determinado doc
		for doc in docs:    #percorrendo os documentos que tem aquela palavra
			cnt.clear()	
			for palavra in dicionario[str(doc)]:
				cnt[palavra] += 1
				
			tupla = ('doc_'+ str(doc), cnt[termo])
			if tupla not in indice_refinado[termo][idf]: #se o dicionario não tiver a tupla (doc, tf_termo) adiciona
				indice_refinado[termo][idf].append(('doc_'+ str(doc), cnt[termo]))

	return indice_refinado

	
"""Calcula a frenquencia de uma palavra num doc"""
def BM25(k, tf, M, idf):
	
	frequency =  (((k + 1) * tf) / tf + k) * (math.log(M+1) * idf)
	
	return frequency
	
def criaRanking(consulta):
	resultado = "Consulta: " + consulta
	
	consulta = consulta.lower().split()
	
	M = len(dicionario)
	
	dic_frequencia = {}
	
	for palavra in consulta:
		if indice_refinado.has_key(palavra):
			idf = indice_refinado[palavra].keys()[0]
			lista_tfs = indice_refinado[palavra][idf]
			for doc in lista_tfs:
				tf = doc[1]
				bm = BM25(10, tf, M, idf)
				if dic_frequencia.has_key(doc[0]):
					dic_frequencia[doc[0]] += bm
				else:
					dic_frequencia[doc[0]] =  bm
	
	
			
	return dic_frequencia
	
"""
print criaIndiceInvertido(leWiki('oi.txt'))
print ('\n\n')
print criaIndiceRefinado(leWiki("oi.txt"))
print ('\n\n')
print consulta("estrelar Mosaico", leWiki("oi.txt"))"""

criaDict(leWiki("ptwiki-v2.trec"))
criaIndiceInvertido()
print criaIndiceRefinado()
