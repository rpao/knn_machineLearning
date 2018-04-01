from vdm import vdm
from euclidiana import euclidiana
class hvdm(object):
    def config(self, conjunto_treino, classe_treino, peso = False, q = 1):
        self.conjunto_treino = conjunto_treino
        self.classe_treino = classe_treino
        self.peso = peso
        self.q = q
        
        self.define_tipo_atributos()
        self.configurar_subconjuntos()
        self.configurar_vdm()

    def define_tipo_atributos(self):
        self.att_categorico = []
        self.att_numerico = []
        
        for i in range(len(self.conjunto_treino[0])):
            if type(self.conjunto_treino[0][i]) == type('str'): self.att_categorico.append(i)
            else: self.att_numerico.append(i)

    def configurar_subconjuntos(self):
        self.categorico = []
        self.numerico = []

        ## criar submatrizes separando categoricos de numericos
        for i in range(len(self.conjunto_treino)):
            linha_c = []
            linha_n = []
            
            for j in range(len(self.conjunto_treino[i])):
                if j in self.att_categorico: linha_c.append(self.conjunto_treino[i][j])
                else: linha_n.append(self.conjunto_treino[i][j])

            self.categorico.append(linha_c)
            self.numerico.append(linha_n)

    def resultado_vdm(self, matriz, tupla):
        med = 0
        for linha in matriz:
            for elemento in linha:
                if elemento[0] == tupla:
                    return elemento[1]
                else:
                    med += elemento[1]
        return med/(len(matriz)*len(matriz[0]))
    
    def configurar_vdm(self):
        self.VDM = vdm()
        self.matriz_vdm = self.VDM.config(self.categorico, self.classe_treino,self.q,self.peso)

    def classificar(self, entrada):
        e = euclidiana()
        
        ## separando atributos categoricos de numericos
        entrada_c = []
        entrada_n = []
        for i in range(len(entrada)):
            if i in self.att_categorico: entrada_c.append(entrada[i])
            else: entrada_n.append(entrada[i])

        lista = []
        for i in range(len(self.numerico)):
            d_categorico = 0
            for j in range(len(entrada_c)):
                tupla = (entrada_c[j],self.categorico[i][j])
                d_categorico +=  self.resultado_vdm(self.matriz_vdm[j], tupla)
                
            d_numerico = e.calcular(entrada_n, self.numerico[i],self.peso)
            lista.append((self.classe_treino[i],d_categorico+d_numerico))

        return lista
