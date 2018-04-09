import math
import random
import operator
import numpy as np

class lvq1(object):
    """
    Atributos:
        database: base de dados utilizada para construir o conjunto de prototipos
        qtd_prototipos: numero de prototipos selecionados
    """
    def get_prototipos(self, database, qtd_prototipos = 2, tx_aprendizagem = 0.01):
        if len(database) == 0: raise IndexError
                      
        db = np.array(database)
        self.classes = list({x for x in set(db.transpose()[len(database[0])-1])})

        self.database = self.separar_classes(database)
        
        self.qtd_prototipos = qtd_prototipos
        
        self.qtdP_classe = self.qtd_prototipos/len(self.classes)

        if qtd_prototipos < 2 or self.qtd_prototipos > len(database): raise ValueError
        
        for c in self.database:
            if self.qtdP_classe > len(c):
                raise ValueError

        self.conjunto_prototipos = self.definir_prototipos(self.database)
        self.treinar_prototipos(tx_aprendizagem)

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

    def definir_prototipos(self, database):
        conjunto_prototipos = []        

        for subconjunto in database:
            for i in range(self.qtdP_classe):
                inst = random.choice(subconjunto)
                conjunto_prototipos.append(inst)
                subconjunto.remove(inst)
            
        return conjunto_prototipos

    ## calcula a distancia euclidiana
    def euclidiana(self, instancia1, instancia2):
        distancia = 0
        for i in range(len(instancia1)-1):
            if instancia1[i] == None or instancia2[i] == None: distancia += 0
            else: distancia += pow((float(instancia1[i])-float(instancia2[i])),2)
        return math.sqrt(distancia)
    
    def treinar_prototipos(self, a):
        for c in range(len(self.conjunto_prototipos)):
            
            lista_vizinhos = []
            
            for conjunto in self.database:
                for i in range(len(conjunto)):
                    distancia = self.euclidiana(self.conjunto_prototipos[c], conjunto[i])
                    lista_vizinhos.append((distancia, conjunto[i]))

            ## ordena de acordo com a distancia
            lista_vizinhos.sort(key = operator.itemgetter(0))

            vizinho = lista_vizinhos[0][1]
            
            if vizinho[len(vizinho)-1] == self.conjunto_prototipos[c][len(self.conjunto_prototipos[c])-1]:
                for i in range(len(self.conjunto_prototipos[c])-1):
                    self.conjunto_prototipos[c][i] = self.conjunto_prototipos[c][i] + a*(vizinho[i] - self.conjunto_prototipos[c][i])
            else:
                for i in range(len(self.conjunto_prototipos[c])-1):
                    self.conjunto_prototipos[c][i] = self.conjunto_prototipos[c][i] - a*(vizinho[i] - self.conjunto_prototipos[c][i])
     
