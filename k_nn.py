import math
import operator
import numpy as np

from vdm import vdm
from hvdm import hvdm
from euclidiana import euclidiana

distancia_euclidiana = 'euclidiana'
distancia_hvdm = 'hvdm'
distancia_vdm = 'vdm'

class k_nn(object):
    def config(self, conjunto_treino, classe_treino, peso = False, d = 'distancia_euclidiana', vdm_q = 1):
        self.conjunto_treino = conjunto_treino
        self.classe_treino = classe_treino
        self.peso = peso
        self.d = d.lower()
        self.q = vdm_q        
        
        if d != distancia_euclidiana and d != distancia_hvdm and d != distancia_vdm:
            raise NameError('Distancia desconhecida')

        if d == distancia_vdm:
            self.q = vdm_q
            
            self.VDM = vdm()
            self.VDM.config(self.conjunto_treino, self.classe_treino, self.q, self.peso)

        if d == distancia_hvdm:
            self.q = vdm_q
            self.HVDM = hvdm()
            self.HVDM.config(self.conjunto_treino, self.classe_treino, self.q, self.peso)

    def por_euclidiana(self):
        Euclidiana = euclidiana()
        
        lista_vizinhos = []
        
        for i in range(len(self.conjunto_treino)):
            dist = Euclidiana.calcular(self.entrada, self.conjunto_treino[i], self.peso)
            
            if dist == 0: return [self.classe_treino[i]]

            lista_vizinhos.append((self.classe_treino[i],dist))

        return lista_vizinhos

    def get_vizinhos(self):
        ## Euclidiana (lista_vizinhos = [(classe,distancia)])
        if self.d == distancia_euclidiana: lista_vizinhos = self.por_euclidiana()
        elif self.d == distancia_hvdm: lista_vizinhos = self.HVDM.classificar(self.entrada)
        elif self.d == distancia_vdm: lista_vizinhos = self.VDM.calculate(self.entrada)        
        
        ## ordena de acordo com a distancia
        lista_vizinhos.sort(key = operator.itemgetter(1))

        ## se for com peso, inverte a lista de vizinhos (maior peso sera escolhido)
        if self.peso: lista_vizinhos.reverse()

        ## seleciona os K vizinhos mais proximos
        vizinhos = []
        if len(lista_vizinhos) < self.k:
            for valor in lista_vizinhos: vizinhos.append(valor[0])

        else:
            for i in range(self.k):
                vizinhos.append(lista_vizinhos[i][0])
                
        return vizinhos
    
    def classificar(self, entrada, k = 1):
        self.k = k
        self.entrada = entrada

        if self.k > len(self.conjunto_treino):
            raise NameError("Valor de k grande para o conjunto de treinamento existente")

        if len(self.entrada) != len(self.conjunto_treino[0]):
            raise NameError("Quantidade de atributos da entrada incompativel com a quantidade de atributos no conjunto de treinamento")

        ## obtem as classes dos vizinhos por ordem de proximidade
        vizinhos = self.get_vizinhos()

        ## lista de classes possiveis
        classes_possiveis = list({x for x in set(vizinhos)})

        ## numero de ocorrencias de cada classe
        freq_classe = []
        for classe in classes_possiveis:
            freq_classe.append(vizinhos.count(classe))

        ## obtem a maior frequencia encontrada
        maior_freq = max(freq_classe)

        ## obtem a posicao da classe escolhida
        escolhida = freq_classe.index(maior_freq)
        
        return classes_possiveis[escolhida]

        
      
