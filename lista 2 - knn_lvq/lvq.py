from lvq1 import lvq1
from lvq2 import lvq2
from lvq3 import lvq3

class lvq(object):
    def config (self, atributos, coluna_alvo, p, versao = 1, a = 0.01, e = 0.5):
        self.database = self.unir(atributos, coluna_alvo)
        self.p = p
        self.a = a
        self.e = e
        
        if versao == 1:
            self.lvq = lvq1()
            self.lvq.config(self.database, self.p, self.a)
            
        elif versao == 2:
            self.lvq = lvq2()
            self.lvq.config(self.database, self.p, self.a)
            
        elif versao == 3:
            self.lvq = lvq3()
            self.lvq.config(self.database, self.p, self.a, self.e)
            
        else: raise NameError

    def unir(self, att, classe):
        database = []
        for i in range(len(att)):
            vetor = []
            for j in range(len(att[i])):
                vetor.append(att[i][j])
            vetor.append(classe[i])
            database.append(vetor)

        return database

    def get_prototipos(self):
        return self.lvq.get_prototipos_att_classe()
            
