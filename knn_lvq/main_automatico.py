import time

from k_nn import k_nn
from lvq import lvq
from arquivo import arquivo

from sklearn.model_selection import KFold

def ler_lista_inteiro (mensagem, valor_minimo = None, valor_maximo = None):
    print (mensagem)
    if valor_minimo != None and valor_maximo != None:
        string = '(Digite apenas inteiros de '+repr(valor_minimo)+' ate '+repr(valor_maximo)+' separados por espaco simples)\n>> '
    elif valor_minimo != None:
        string = '(Digite apenas inteiros iguais ou maiores que '+repr(valor_minimo)+' separados por espaco simples)\n>> '
    else:
        string = '(Digite apenas inteiros iguais ou menores que '+repr(valor_maximo)+' separados por espaco simples)\n>> '

    while True:
        entrada = raw_input(string).split(' ')

        try:
            lista = list({int(x) for x in set(entrada)})
            for inteiro in lista:
                if valor_minimo != None and inteiro < valor_minimo: raise ZeroDivisionError
                if valor_maximo != None and inteiro > valor_maximo: raise ZeroDivisionError

            return lista
            
        except ValueError: print ('\n[Erro] Utilize apenas numeros inteiros e espacos simples\n>> ')
        except ZeroDivisionError:
            print('\n[Erro] Existe(m) valor(es) fora do limite definido')
            
            
def ler_inteiro(mensagem, valor_minimo = None, valor_maximo = None):
    print (mensagem)

    if valor_minimo != None and valor_maximo != None:
        string = '(Digite apenas um inteiro entre '+repr(valor_minimo)+' e '+repr(valor_maximo)+')\n>> '
    elif valor_minimo != None:
        string = '(Digite apenas um inteiro maior ou igual a '+repr(valor_minimo)+')\n>> '
    else:
        string = '(Digite apenas um inteiro menor ou igual a '+repr(valor_maximo)+')\n>> '

    while True:
        try:
            inteiro = int(raw_input(string))
            if valor_minimo != None and inteiro < valor_minimo: raise ValueError
            if valor_maximo != None and inteiro > valor_maximo: raise ValueError
            else: return inteiro
            
        except ValueError:
            print('\n[Erro] Valor fora do limite definido')

def ler_float(mensagem, valor_minimo = None, valor_maximo = None):
    print (mensagem)

    if valor_minimo != None and valor_maximo != None:
        string = '(Digite apenas um float entre '+repr(valor_minimo)+' e '+repr(valor_maximo)+')\n>> '
    elif valor_minimo != None:
        string = '(Digite apenas um float maior ou igual a '+repr(valor_minimo)+')\n>> '
    else:
        string = '(Digite apenas um float menor ou igual a '+repr(valor_maximo)+')\n>> '
        
    while True:
        try:
            valor = float(raw_input(string))
            if valor_minimo != None and valor < valor_minimo: raise ValueError
            if valor_maximo != None and valor > valor_maximo: raise ValueError
            else: return valor
            
        except ValueError:
            print('\n[Erro] Valor fora do limite definido')

def calcular_acerto(classficacao, coluna_alvo):
    acerto = 0
    for i in range(len(classificacao)):
        for j in range(len(classificacao[i])):
            if classificacao[i][j] == coluna_alvo[i][j]: acerto += 1
    return acerto

arquivo = arquivo()

lista_kf = [10]
lista_kn = [1,3]
qtd_testes = 20

a = 0.001
e = 0.05
    
for arq in ['data\kc2.csv','data\pc1.csv']:
    atributos, coluna_alvo = arquivo.abrir(arq)
    qtd_instancias = float(len(coluna_alvo))
    if arq == 'data\kc2.csv': p = 100
    else: p = 50
        
    for mode_LVQ in [1, 2, 3]:
        print '\n*****************************************************************\n'
        print 'Arquivo: ',arq
        print 'LVQ: ',mode_LVQ
        print 'Quantidade de testes: ', qtd_testes
        print 'Quantidade de instancias: ', qtd_instancias
        print 'Quantidade de Prototipos: ', p, '\n'
        print 'Taxa de aprendizagem: ', a
        print 'Epsilon: ',e

        tempo_total = time.clock()
        
        for kf in lista_kf:
            
            print 'kf: ',kf
            
            for kn in lista_kn:
                
                print 'kn: ', kn
                
                for teste_atual in range(qtd_testes):
                    
                    tempo_teste_atual = time.clock()

                    ## definindo o kfold
                    kfold = KFold(n_splits = kf)

                    ## definindo k-nn
                    knn = k_nn()

                    ## numero de acertos
                    acertos = 0.0

                    ## vetor que guarda as classificacoes
                    classificacoes = []

                    ## tempo medio de execucao da classificacao de cada instancia
                    tempo_medio = 0
                                        
                    ## execucao da classificacao
                    ## para cada subconjunto gerado pelo kfold, um eh guardado em treinamento e outro em teste
                    for indice_treinamento, indice_teste in kfold.split(atributos):

                        ## sem selecao de prototipos, utiliza conjunto completo
                        if mode_LVQ == 4:
                            tempo_LVQ = 0
                            X_train, X_test = atributos[indice_treinamento], atributos[indice_teste]
                            y_train, y_test = coluna_alvo[indice_treinamento], coluna_alvo[indice_teste]

                        ## obtem o conjunto de prototipos se lvq tiver sido selecionado
                        else:
                            tempo_LVQ = time.clock()
                            
                            sLVQ = lvq()
                            sLVQ.config(atributos[indice_treinamento], coluna_alvo[indice_treinamento], p, mode_LVQ, a, e)
                            
                            X_train, y_train = sLVQ.get_prototipos()
                            X_test, y_test = atributos[indice_teste], coluna_alvo[indice_teste]

                            tempo_LVQ = time.clock() - tempo_LVQ
        

                        knn.config(X_train, y_train)
                        
                        start_time = time.clock()
                        
                        for i in range(len(X_test)):
                            classe = knn.classificar(X_test[i],kn)
                            if classe == y_test[i]: acertos += 1.0
                            classificacoes.append((X_test, y_test, classe))

                        tempo_medio += time.clock() - start_time
                    
                    taxa_acertos = acertos/qtd_instancias
                    tempo_medio = tempo_medio/qtd_instancias
                    tempo_teste_atual = time.clock () - tempo_teste_atual
                    
                    #print ('[Teste '+repr(teste_atual)+']\tTaxa de Acerto: '+repr(round(taxa_acertos,4))+'\tTempo medio de classificacao'+repr(round(tempo_medio,3)))+'\nTempo de Selecao de Prototipos: '+repr(tempo_LVQ)+' segundos.')
                    print (repr(round(taxa_acertos,4))+','+repr(round(tempo_medio,3))+','+repr(tempo_LVQ))
                    
        tempo_total = time.clock() - tempo_total
        print ('\nTempo total: '+repr(tempo_total)+' segundos.')
