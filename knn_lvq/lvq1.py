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
    def config(self, database, qtd_prototipos, taxa_aprendizagem = 0.01):
        if len(database) == 0: raise IndexError
        
        if qtd_prototipos < 2 or qtd_prototipos > len(database):
            raise ValueError

        self.database = database
        self.p = qtd_prototipos
        self.a = taxa_aprendizagem
        
        self.conjunto_prototipos = self.definir_prototipos()
        
##        print 'Configurando:'
##        print '\tdatabase: ',self.database
##        print '\tp: ',self.p
##        print '\ta: ',self.a
##        print '\tprototipos s/ treino: ',self.conjunto_prototipos

        self.treinar_prototipos()
##        print '\tprototipos c/ treino: ',self.conjunto_prototipos
        
    def definir_prototipos(self):
        conjunto_prototipos = []
        ultima_classe = None
        cont = 0
        
        while cont < self.p:
            inst = random.choice(self.database)
            if ultima_classe != inst[len(inst)-1]:
                conjunto_prototipos.append(inst)
                self.database.remove(inst)
                ultima_classe = inst[len(inst)-1]
                cont += 1

        for inst in conjunto_prototipos:
            self.database.append(inst)
                
        return conjunto_prototipos
    
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
            
            ## ordena de acordo com a distancia
            lista_prototipos.sort(key = operator.itemgetter(0))

            prototipo = lista_prototipos[0][1]

            classePrototipo = prototipo[len(prototipo)-1]
            classeElemento = instancia[len(instancia)-1]

            if classePrototipo == classeElemento:
                for k in range(len(instancia)-1):
                    prototipo[k] = prototipo[k] + self.a*(instancia[k] - prototipo[k])

            else:
                for k in range(len(instancia)-1):
                    prototipo[k] = prototipo[k] - self.a*(instancia[k] - prototipo[k])


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
