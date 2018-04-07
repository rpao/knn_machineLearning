import math
import numpy as np
from value_difference_metric import value_difference_metric

class vdm(object):
    
    def config(self, dataset, cla_dataset, q, pesos = False):

        ## discretizar
        for i in range(len(dataset)):
            for j in range(len(dataset[i])):
                if type(dataset[i][j]) != type('str'):
                    if (10*dataset[i][j])%10 >= 5: dataset[i][j] = math.ceil(dataset[i][j])
                    else: dataset[i][j] = math.floor(dataset[i][j])
                    
        if type(dataset) != type(np.array(0)):
            self.dataset = np.array(dataset)
        else:
            self.dataset = dataset
            
        self.cla_dataset = cla_dataset
        self.q = q
        self.pesos = pesos
        
        self.result = self.calculate_matriz_vdm()
        return self.result

    def converter(self, resultado):
        matriz_ext = []
        
        for matriz in resultado:
            matriz_int = []
            for i in range(len(matriz)):
                linha = []
                for j in range(len(matriz[i])):
                    if self.pesos:
                        if matriz[i][j][1] == 'na':
                            try: valor = (matriz[i][j][0], 1/pow(matriz[j][i][1],2))
                            except ZeroDivisionError: valor = (matriz[i][j][0], 1000)
                        else:
                            try: valor = (matriz[i][j][0], 1/pow(matriz[i][j][1],2))
                            except ZeroDivisionError: valor = (matriz[i][j][0], 1000)

                    else:
                        if matriz[i][j][1] == 'na': valor = (matriz[i][j][0],matriz[j][i][1])
                        else: valor = (matriz[i][j][0],matriz[i][j][1])
                    linha.append(valor)
                matriz_int.append(linha)
            matriz_ext.append(matriz_int)

        return matriz_ext
        
    def calculate_matriz_vdm(self):
        
        att_dataset_aux = self.dataset.transpose()

        valores_att = []
        for linha in att_dataset_aux:
            lista = list({x for x in set(linha)})
            lista.sort()
            valores_att.append(lista)

        v = value_difference_metric()
        v.config(self.dataset, self.cla_dataset)
        matriz_ext = []

        for i in range(len(valores_att)):
            matriz = []
            for j in range(len(valores_att[i])):
                linha = []
                for k in range(len(valores_att[i])):
                    if k >= j:
                        vdm = round(v.calculate(valores_att[i][j], valores_att[i][k],i,self.q),4)                            
                        linha.append(((valores_att[i][j], valores_att[i][k]),vdm))
                    else:
                        linha.append(((valores_att[i][j], valores_att[i][k]),'na'))
                matriz.append(linha)
            matriz_ext.append(matriz)

        return self.converter(matriz_ext)

    def resultado_vdm(self, matriz, tupla):
        med = 0
        for linha in matriz:
            for elemento in linha:
                if elemento[0] == tupla:
                    return elemento[1]
                else:
                    med += elemento[1]
        return med/(len(matriz)*len(matriz[0]))
    
    def calculate(self, entrada):
        for i in range(len(entrada)):
            if type(entrada[i]) != type('str'):
                if (10*entrada[i])%10 >= 5: entrada[i] = math.ceil(entrada[i])
                else: entrada[i] = math.floor(entrada[i])
                
        dVDM = []
        for i in range(len(self.dataset)):
            dist = 0
            for j in range(len(entrada)):
                tupla = (entrada[j],self.dataset[i][j])                
                dist += self.resultado_vdm(self.result[j], tupla)
                if dist == 0:
                    return [(self.cla_dataset[i],dist)]
                
            dVDM.append((self.cla_dataset[i],dist))
        return dVDM
