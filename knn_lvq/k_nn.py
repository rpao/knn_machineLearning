import math
import operator
import numpy as np

class k_nn(object):

    ## configura o conjunto de treinamento e sua coluna de classes
    def config(self, conjunto_treinamento, classe_treinamento):
        self.conjunto_treinamento = conjunto_treinamento
        self.classe_treinamento = classe_treinamento
        return True

    ## calcula a distancia euclidiana
    def euclidiana(self, instancia1, instancia2):
        distancia = 0
        for i in range(len(instancia1)):
            if instancia1[i] == None or instancia2[i] == None: distancia += 0
            else: distancia += pow((float(instancia1[i])-float(instancia2[i])),2)
        return math.sqrt(distancia)

    ## calcula a distancia entre a entrada e todos os elementos do conjunto de treinamento
    ## retorna uma lista com a distancia e a classe
    def get_vizinhos(self):
        lista_vizinhos = []

        for i in range(len(self.conjunto_treinamento)):
            distancia = self.euclidiana(self.entrada, self.conjunto_treinamento[i])

            if distancia == 0: return [(0,self.classe_treinamento[i])]

            lista_vizinhos.append((distancia, self.classe_treinamento[i]))

        ## ordena de acordo com a distancia
        lista_vizinhos.sort(key = operator.itemgetter(0))

        ## seleciona os K vizinhos mais proximos
        
        if len(lista_vizinhos) < self.k:
            return lista_vizinhos

        else: vizinhos = lista_vizinhos[:self.k]
                
        return vizinhos

    ## classificar uma entrada de acordo com os k vizinhos mais proximos
    ## retorna a classe mais frequente
    def classificar(self, entrada, k):
        self.entrada = entrada
        self.k = k

        if self.k > len(self.conjunto_treinamento):
            raise NameError("Valor de k grande para o conjunto de treinamento existente")

        if len(self.entrada) != len(self.conjunto_treinamento[0]):
            raise NameError("Quantidade de atributos da entrada incompativel com a quantidade de atributos no conjunto de treinamento")

        ## obtem todos os k vizinhos mais proximos
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
        
        return classes_possiveis[escolhida][1]

        

        

        
        
        
      
