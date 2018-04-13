import math
import random
import operator
import numpy as np
from lvq1 import lvq1

class lvq3(object):
    """
    Atributos:
        database: base de dados utilizada para construir o conjunto de prototipos
        qtd_prototipos: numero de prototipos selecionados
        a: taxa de aprendizagem
    """
    
    def config(self, database, qtd_prototipos = 2, taxa_aprendizagem = 0.01, epsilon = 0.5):
        if len(database) == 0: raise IndexError

        if qtd_prototipos < 2 or qtd_prototipos > len(database): raise ValueError

        if epsilon < 0 or epsilon > 1: raise TypeError

        self.database = database
        self.p = qtd_prototipos
        self.a = taxa_aprendizagem
        self.e = epsilon

        lvq = lvq1()
        lvq.config(database, self.p, self.a)
        self.conjunto_prototipos = lvq.get_prototipos()

##        print 'LVQ3.0 - Configurando:'
##        print '\tdatabase: ',self.database
##        print '\tp: ',self.p
##        print '\ta: ',self.a
##        print '\te: ',self.e
##        print '\tprototipos s/ treino: ',self.conjunto_prototipos

        self.treinar_prototipos
##        print '\tprototipos c/ treino: ',self.conjunto_prototipos

    ## calcula a distancia euclidiana
    def euclidiana(self, instancia1, instancia2):
        distancia = 0
        for i in range(len(instancia1)-1):
            if instancia1[i] == None or instancia2[i] == None: distancia += 0
            else: distancia += pow((float(instancia1[i])-float(instancia2[i])),2)
        return math.sqrt(distancia)
    
    def treinar_prototipos(self):
        for instancia in self.database:
            lista_prototipos = []

            for prototipo in self.conjunto_prototipos:
                distancia = self.euclidiana(instancia, prototipo)
                lista_prototipos.append((distancia, prototipo))

            lista_prototipos.sort(key = operator.itemgetter(0))

            prototipo1 = lista_prototipos[0][1]
            prototipo2 = lista_prototipos[1][1]

            classe1 = prototipo1[len(prototipo1)-1]
            classe2 = prototipo2[len(prototipo2)-1]
            classeElemento = conjunto[i][len(instancia)-1]

            if classe1 != classe2 and classe1 == classeElemento:
                for k in range(len(conjunto[i])-1):
                    prototipo1[k] = prototipo1[k] + self.a*(instancia[k] - prototipo1[k])
                    prototipo2[k] = prototipo2[k] - self.a*(instancia[k] - prototipo2[k])

            elif classe1 != classe2 and classe2 == classeElemento:
                for k in range(len(conjunto[i])-1):
                    prototipo1[k] = prototipo1[k] - self.a*(instancia[k] - prototipo1[k])
                    prototipo2[k] = prototipo2[k] + self.a*(instancia[k] - prototipo2[k])
                    
            elif classe1 == classeElemento and classe2 == classeElemento:
                for k in range(len(conjunto[i])-1):
                    prototipo1[k] = prototipo1[k] + self.e*self.a*(instancia[k] - prototipo1[k])
                    prototipo2[k] = prototipo2[k] + self.e*self.a*(instancia[k] - prototipo2[k])


    def get_prototipos_att_classe(self):
        prot_att = []
        prot_classe = []

        for prototipo in self.conjunto_prototipos:
            prot_classe.append(prototipo[len(prototipo)-1])
            vetor = []
            for i in range(len(prototipo)-1):
                vetor.append(prototipo[i])
            prot_att.append(vetor)
            
        return prot_att, prot_classe
    
    def get_prototipos(self):
        return self.conjunto_prototipos
