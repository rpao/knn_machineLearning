import time

from k_nn import k_nn
from lvq1 import lvq1
from arquivo import arquivo

from sklearn.model_selection import KFold

def ler_lista_inteiro (mensagem, valor_minimo = None, valor_maximo = None):
    print (mensagem)
    if valor_minimo != None and valor_maximo != None:
        string = '\nDigite apenas inteiros de '+repr(valor_minimo)+' ate '+repr(valor_maximo)+' separados por espaco simples\n>> '
    elif valor_minimo != None:
        string = '\nDigite apenas inteiros iguais ou maiores que '+repr(valor_minimo)+' separados por espaco simples\n>> '
    else:
        string = '\nDigite apenas inteiros iguais ou menores que '+repr(valor_maximo)+' separados por espaco simples\n>> '

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
        string = '\nDigite apenas um inteiro entre '+repr(valor_minimo)+' e '+repr(valor_maximo)+'\n>> '
    elif valor_minimo != None:
        string = '\nDigite apenas um inteiro maior ou igual a '+repr(valor_minimo)+'\n>> '
    else:
        string = '\nDigite apenas um inteiro menor ou igual a '+repr(valor_maximo)+'\n>> '

    while True:
        try:
            inteiro = int(raw_input(string))
            if valor_minimo != None and inteiro < valor_minimo: raise ValueError
            if valor_maximo != None and inteiro > valor_maximo: raise ValueError
            else: return inteiro
            
        except ValueError:
            print('\n[Erro] Valor fora do limite definido')

def calcular_acerto(classficacao, coluna_alvo):
    acerto = 0
    for i in range(len(classificacao)):
        for j in range(len(classificacao[i])):
            if classificacao[i][j] == coluna_alvo[i][j]: acerto += 1
    return acerto

arquivo = arquivo()

str_menu_lvq = 'Selecione o algoritmo:\n1 - Sem Selecao de Prototipos\n2 - LVQ1\n3 - LVQ2.1\n4 - LVQ3'

p = 0

sair = False

while(sair == False):
    erro_arquivo = True
    while erro_arquivo:
        database = raw_input('Caminho completo do arquivo:  ')
        try:
            arquivo.abrir(database)
            erro_arquivo = False
        except IOError as e:
            print(" [Erro "+str(e.args[0])+"] "+str(e.args[1]))
        
    lista_kf = ler_lista_inteiro('\nPara o k-fold',2)
    lista_kn = ler_lista_inteiro('\nPara o k-NN',1)
    qtd_testes = ler_inteiro('\nQuantidade de testes: ',1)

    print (str_menu_lvq)
    mode_LVQ = ler_inteiro("", 1, 4)
            
    if mode_LVQ != 1: p = ler_inteiro('\nQuantidade de prototipos: ',1)

    try:
        tempo_total = time.clock()
        tempo_LVQ = 0
        
        for kf in lista_kf:
            for kn in lista_kn:
                print('k-Fold: '+repr(kf)+'\t k-NN: '+repr(kn))
                
                for teste_atual in range(qtd_testes):
                    

                    if mode_LVQ == 1:
                        atributos, coluna_alvo = arquivo.get_att_classe()

                    elif mode_LVQ == 2:
                        
                        tempo_LVQ = time.clock()

                        db = arquivo.get_dataset()
                        lvq = lvq1()
                        lvq.config(db, p)
                        atributos, coluna_alvo = lvq.get_prototipos_att_classe()

                        tempo_LVQ = time.clock() - tempo_LVQ
                        print 'LVQ 1.0'
                        
                    elif mode_LVQ == 3:
                        tempo_LVQ = time.clock()

                        db = arquivo.get_dataset()
                        lvq = lvq2()
                        lvq.config(db, p)
                        atributos, coluna_alvo = lvq.get_prototipos_att_classe()
                        
                        tempo_LVQ = time.clock() - tempo_LVQ
                        print 'LVQ 2.1'
                        
                    elif mode_LVQ == 4:
                        tempo_LVQ = time.clock()

                        db = arquivo.get_dataset()
                        lvq = lvq3()
                        lvq.config(db, p)
                        atributos, coluna_alvo = lvq.get_prototipos_att_classe()
  
                        tempo_LVQ = time.clock() - tempo_LVQ
                        print 'LVQ 3.0'

                    for i in range(len(atributos)):
                        print atributos[i],' - ', coluna_alvo[i],'\n'
    
                    raise ZeroDivisionError
                
                    qtd_instancias = float(len(coluna_alvo))
                    
                    kfold = KFold(n_splits = kf)
                    knn = k_nn()

                    acertos = 0.0
                    
                    classificacoes = []
                    
                    tempo_medio = 0
                   
                    for indice_treinamento, indice_teste in kfold.split(atributos):
                        X_train, X_test = atributos[indice_treinamento], atributos[indice_teste]
                        y_train, y_test = coluna_alvo[indice_treinamento], coluna_alvo[indice_teste]

                        knn.config(X_train, y_train)
                        
                        start_time = time.clock()
                        
                        for i in range(len(X_test)):
                            classe = knn.classificar(X_test[i],kn)
                            if classe == y_test[i]: acertos += 1.0
                            classificacoes.append((X_test, y_test, classe))

                        tempo_medio += time.clock() - start_time
                            
                    tempo_medio = tempo_medio/qtd_instancias
                    
                    taxa_acertos = acertos/qtd_instancias

                    tempo_total = time.clock() - tempo_total
                    
                    print (repr(teste_atual)+','+repr(round(taxa_acertos,4))+','+repr(round(tempo_medio,3)))

                    ##print ('['+repr(teste_atual)+']\tTaxa de acerto: '+repr(round(taxa_acertos,4))+'\n\tTempo Medio de Execucao Por Instancia do Conjunto de Teste: '+repr(round(tempo_medio,3))+' segundos')

                    print ('Tempo de Selecao de prototipos: '+repr(tempo_LVQ)+'segundos.')
                    
        print 'tempo total: ',tempo_total
    except IOError as e:
        print(" [Erro "+str(e.args[0])+"] "+str(e.args[1]))

    continuar = raw_input('Encerrar S/N?  ').upper()
    if continuar == 'S': sair = True
    else: sair = False
