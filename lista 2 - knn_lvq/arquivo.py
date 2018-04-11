import csv
import random
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

class arquivo(object):

    ## abre o arquivo e armazena os dados numa matriz 'dataset'
    def abrir(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        
        ## obtendo dados do arquivo (csv)
        with open(self.nome_arquivo, 'rb') as csvfile:
            
            full_data = csv.reader(csvfile)
            
            ## armazenando dados em uma lista
            self.dataset_original = list(full_data)

            ## aleatorizando o conjunto lido
            self.dataset = []
            while len(self.dataset_original) != 0:
                inst = random.choice(self.dataset_original)
                self.dataset.append(inst)
                self.dataset_original.remove(inst)
        
        self.coluna_alvo = len(self.dataset[0])-1

        return self.get_att_classe()

    ## obtem os k conjuntos
    def get_dataset (self):
        elementos = []

        ## Separacao de atributos e coluna alvo
        for line in self.dataset:
            values = []
            for i in range(len(line)):
                try: values.append(float(line[i]))
                except ValueError:
                    if line[i] == '?': values.append(None)
                    else: values.append(line[i])
            elementos.append(values)
            
        return elementos
    
    def get_att_classe(self):
        atributos = []
        classes = []

        ## Separacao de atributos e coluna alvo
        for line in self.dataset:
            values = []
            for i in range(len(line)):
                if i != self.coluna_alvo:
                    try: values.append(float(line[i]))
                    except ValueError:
                        if line[i] == '?': values.append(None)
                        else: values.append(line[i])
            atributos.append(values)
            classes.append(line[self.coluna_alvo])

        return np.array(atributos), np.array(classes)
