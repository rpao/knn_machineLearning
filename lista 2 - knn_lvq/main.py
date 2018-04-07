import numpy as np
from k_nn import k_nn
from arquivo import arquivo
from sklearn.model_selection import KFold
    
def ler_inteiro(string, valor_minimo = 1):
    while True:
        try:
            inteiro = int(raw_input(string))
            if inteiro < valor_minimo: raise ValueError
            else: break
            
        except ValueError: print('Deve ser inteiro maior ou igual a '+str(valor_minimo))
    return inteiro

def calcular_acerto(classficacao, coluna_alvo):
    acerto = 0
    for i in range(len(classificacao)):
        for j in range(len(classificacao[i])):
            if classificacao[i][j] == coluna_alvo[i][j]: acerto += 1
    return acerto
            
nome_arquivo = raw_input('Caminho completo do arquivo:  ')
kf = ler_inteiro('k-fold: ', 2)
kn = ler_inteiro('k-Neighbors: ')
qtd_testes = ler_inteiro('Quantidade de testes: ')

opcao_invalida = True
while opcao_invalida:
    mode_LVQ = ler_inteiro('Selecione o algoritmo:\n1 - LVQ1\n2 - LVQ2.1\n3 - LVQ3\n4 - Sem Selecao de Prototipos:: ')

    if mode_LVQ < 1 or mode_LVQ > 4:
        print ('**** Opcao invalida ****')
        opcao_invalida = True

    else: opcao_invalida = False
    
if mode_LVQ != 4: qtd_prototipos = ler_inteiro('Quantidade de prototipos: ')

try:
    arquivo = arquivo()

    for teste_atual in range(qtd_testes):
    
        atributos, coluna_alvo = arquivo.abrir(nome_arquivo)

        qtd_instancias = float(len(coluna_alvo))
            
        if mode_LVQ == 1:
            print 'LVQ 1.0'
            
        elif mode_LVQ == 2:
            print 'LVQ 2.1'
            
        elif mode_LVQ == 3:
            print 'LVQ 3.0'

        kfold = KFold(n_splits = kf)
        knn = k_nn()

        acertos = 0.0
        
        classificacoes = []
        
        for indice_treinamento, indice_teste in kfold.split(atributos):
            X_train, X_test = atributos[indice_treinamento], atributos[indice_teste]
            y_train, y_test = coluna_alvo[indice_treinamento], coluna_alvo[indice_teste]

            knn.config(X_train, y_train)
            
            for i in range(len(X_test)):
                classe = knn.classificar(X_test[i],kn)
                if classe == y_test[i]: acertos += 1.0
                classificacoes.append((X_test, y_test, classe))
                
            
        taxa_acertos = acertos/qtd_instancias

        print ('['+str(teste_atual)+'] Taxa de acerto: '+str(taxa_acertos))
            
except IOError as e:
    print(" [Erro "+str(e.args[0])+"] "+str(e.args[1]))
    print("Encerrando...")
