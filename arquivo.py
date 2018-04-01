import csv
import random
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

class arquivo(object):
    def abrir(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

        try:
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

            self.status = True
            self.coluna_alvo = len(self.dataset[0])-1
                
        except IOError as e:
            print(" [Erro "+str(e.args[0])+"] "+str(e.args[1]))
            self.status = False
            self.coluna_alvo = None
            self.dataset = None

    def split(self,X, y, k):
        splited_x = [X[i::k] for i in range(k)]
        splited_y = [y[i::k] for i in range(k)]
        return splited_x, splited_y

    def get_dataset (self, k = 2):
        if self.status == False: return None, None
        
        X = []
        y = []

        ## Separacao de atributos e coluna alvo
        for line in self.dataset:
            values = []
            
            for i in range(len(line)):
                if i != self.coluna_alvo:
                    try: values.append(float(line[i]))
                    except ValueError:values.append(line[i])

            X.append(values)
            y.append(line[self.coluna_alvo])
            
        att, cla = self.split(X, y, k)

        return att, cla
