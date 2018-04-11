import math
import random
import operator
import numpy as np

from lvq1 import lvq1

class lvq2(object):
    """
    Atributos:
        database: base de dados utilizada para construir o conjunto de prototipos
        qtd_prototipos: numero de prototipos selecionados
    """
    def config(self, database, qtd_prototipos = 2, a = 0.01):
        if len(database) == 0: raise IndexError
                      
        db = np.array(database)
        self.classes = list({x for x in set(db.transpose()[len(database[0])-1])})

        self.database = self.separar_classes(database)
        
        self.qtd_prototipos = qtd_prototipos
        
        self.qtdP_classe = self.qtd_prototipos/len(self.classes)

        self.a = a

        if qtd_prototipos < 2 or self.qtd_prototipos > len(database): raise ValueError
        
        for c in self.database:
            if self.qtdP_classe > len(c):
                raise ValueError

        lvq = lvq1()
        lvq.config(database, self.qtd_prototipos, self.a)
        self.conjunto_prototipos = lvq.get_prototipos()
        self.treinar_prototipos()

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

    def separar_classes(self, database):
        db = []
        for classe in self.classes:
            vetor = []
            for instancia in database:
                if instancia[len(instancia)-1] == classe:
                    vetor.append(instancia)
            db.append(vetor)

        return db   

    ## calcula a distancia euclidiana
    def euclidiana(self, instancia1, instancia2):
        distancia = 0
        for i in range(len(instancia1)-1):
            if instancia1[i] == None or instancia2[i] == None: distancia += 0
            else: distancia += pow((float(instancia1[i])-float(instancia2[i])),2)
        return math.sqrt(distancia)
    
    def treinar_prototipos(self):           
        for conjunto in self.database:
            for i in range(len(conjunto)):
                lista_prototipos = []

                for j in range(len(self.conjunto_prototipos)):
                    distancia = self.euclidiana(conjunto[i], self.conjunto_prototipos[j])
                    lista_prototipos.append((distancia, self.conjunto_prototipos[j]))

                ## ordena de acordo com a distancia
                lista_prototipos.sort(key = operator.itemgetter(0))

                prototipo1 = lista_prototipos[0][1]
                prototipo2 = lista_prototipos[1][1]

                classe1 = prototipo1[len(prototipo1)-1]
                classe2 = prototipo2[len(prototipo2)-1]
                classeElemento = conjunto[i][len(conjunto[i])-1]

                if classe1 == classeElemento and classe2 != classeElemento:
                    for k in range(len(conjunto[i])-1):
                        prototipo1[k] = prototipo1[k] + self.a*(conjunto[i][k] - prototipo1[k])
                        prototipo2[k] = prototipo2[k] - self.a*(conjunto[i][k] - prototipo2[k])

                elif classe1 != classeElemento and classe2 == classeElemento:
                    for k in range(len(conjunto[i])-1):
                        prototipo1[k] = prototipo1[k] - self.a*(conjunto[i][k] - prototipo1[k])
                        prototipo2[k] = prototipo2[k] + self.a*(conjunto[i][k] - prototipo2[k])
