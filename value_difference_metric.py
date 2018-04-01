import math
import numpy as np

class value_difference_metric(object):
    
    def config(self, atributos, classes):
        self.atributos = atributos
        self.classes = classes

    ## Pega valores de uma determinada classe
    def get_classe (self, classe):
        conjunto = []
        
        for i in range(len(self.classes)):
            if self.classes[i] == classe:
                conjunto.append(self.atributos[i])
                
        return conjunto

    def get_all_classes(self):
        all_classes = {x for x in self.classes}
        
        conjunto_classes = []
        for classe in all_classes:
            conjunto_classes.append(classe)
            
        return conjunto_classes

    ## Numero de repeticoes total
    def get_Ni(self, conjunto, valor, indice):
        matriz = np.array(conjunto)
        
        matriz = matriz.transpose()
        
        matriz = matriz.tolist()
        
        return matriz[indice].count(valor)

    ## Numero de repeticoes de um valor dentro de uma classe
    def get_Nic(self, valor, indice, classe):
        conjunto = self.get_classe(classe)
        return self.get_Ni(conjunto, valor, indice)

    def calculate(self, a, b, indice, q):
        if a == b:
            return 0
        
        Nia = float(self.get_Ni(self.atributos, a, indice))
        Nib = float(self.get_Ni(self.atributos, b, indice))

        Niac = []
        Nibc = []

        classes = self.get_all_classes()
        
        for classe in classes:
            valorA = self.get_Nic(a, indice, classe)
            valorB = self.get_Nic(b, indice, classe)
            
            Niac.append(valorA)
            Nibc.append(valorB)

        vdm = 0
        for i in range(len(Niac)):
            vdm += pow(abs(Niac[i]/Nia - Nibc[i]/Nib),q)

        return math.sqrt(vdm)
