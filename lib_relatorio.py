class lib_relatorio(object):
    def set_arquivo(self,arquivo,k_fold):
        self.arquivo = "Arquivo: "+arquivo+" - k-fold = "+str(k_fold)+"\n"

    def set_modo(self,modo):
        self.modo = "Modo: "+modo+"\n"

    def set_distancia(self,distancia):
        self.distancia = "Distancia: "+distancia+"\n"

    def set_k(self,lista_k):
        self.lista_k = lista_k

    def set_tamanho_conjunto(self,tamanho_treinamento, tamanho_teste):
        self.tamanhos = "\nTamanho do conjunto de treinamento = "+str(tamanho_treinamento)
        self.tamanhos += "\nTamanho do conjunto de teste = "+str(tamanho_teste) 

    def set_tempo(self,tempo_treinamento, tempo_classificacao):
        self.tempo_treinamento = "Tempo de Treinamento: "+str(tempo_treinamento)+" segundos\n"

        t = 0
        self.tempo_classificacao = "Tempo de teste individual:\n"
        for i in range(len(tempo_classificacao)):
            t += tempo_classificacao[i]
            self.tempo_classificacao += "k = "+self.lista_k[i]+"\tt = "+str(tempo_classificacao[i])+" segundos\n"

        self.tempo_total = "Tempo total de teste: "+str(t)+" segundos\n"

    def set_taxa_acerto(self,taxa_acerto):
        self.taxas = "Taxas de acerto: \n"
        
        for i in range(len(taxa_acerto)):
            self.taxas += "k = "+self.lista_k[i]+"\t"+str(taxa_acerto[i])+"\n"
            
    def print_tela(self):
        print self.arquivo
        print self.modo
        print self.distancia
        print self.tamanhos
        print self.tempo_treinamento
        print self.tempo_classificacao
        print self.tempo_total
        print self.taxas

    def save(self, nome_relatorio):
        text = []
##        text.append(self.arquivo)
##        text.append(self.modo)
##        text.append(self.distancia)
##        text.append(self.tamanhos)
        text.append(self.taxas)
        text.append(self.tempo_treinamento)
        text.append(self.tempo_classificacao)
        text.append(self.tempo_total)

        ## Escrevendo Relatorio
        try:
##            nome_relatorio = raw_input("nome do relatorio: ")
            ref_relatorio = open('relatorios\\'+nome_relatorio, 'w')
            ref_relatorio.writelines(text)
            ref_relatorio.close()
            print ("Documento "+nome_relatorio+" salvo com sucesso")
        except:
            print ("Erro: Documento "+nome_relatorio+" nao pode ser salvo")
        
            
