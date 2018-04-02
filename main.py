import time

from arquivo import arquivo
from k_nn import k_nn

tempo_treinamento = 0

def calcular_accuracia(predicao, cla_teste):
    acerto = 0
    
    ## calcula a taxa de acertos 
    for i in range(len(predicoes)):
        if predicao[i] == cla_teste[i]: acerto += 1

    ## calcula a acuracia
    accuracia = acerto/float(len(cla_teste))

    return accuracia

def calcula_knn(conjunto_treino, classe_treino, conjunto_teste, lista_k = 1, distancia='Euclidiana', q=1, pesos=False):    
    knn = k_nn()
    knn.config(conjunto_treino, classe_treino, pesos, distancia, q)

    start_time = time.clock()
    
    ## vetor que guarda todas as predicoes realizadas para k
    predicao = []

    ## obtem classe para cada instancia do conjunto de teste
    for entrada in conjunto_teste:
        classe_escolhida = knn.classificar(entrada, k)
        predicao.append(classe_escolhida)

    ## tempo de execucao do knn
    tempo_predicao = time.clock() - start_time

    return predicao, tempo_predicao        

modo_algoritmo = ['k-NN','k-NN ponderado']
modo_distancia = ['euclidiana', 'hvdm', 'vdm']

r_exit = True

while(r_exit):
    nome_arquivo = raw_input("Informe o caminho do arquivo:  ")
    
    ## obtem numero de repeticoes
    while(True):
        try:
            qtd_testes = int(raw_input("quantidade de testes:  "))
            break        
        except ValueError: print ('\nOpcao invalida\n')

    ## obtem valor para kn
    lista_k = raw_input("Informe quantidade de vizinhos (se mais de um, siga o exemplo: 1 2 3..): ").split(' ')
    
    ## obtem valor para kf
    lista_kf = raw_input('Informe quantidade de conjuntos para o k-fold (valor minimo eh 2; se mais de um, siga o exemplo: 2 3 4..: ').split(' ')
    
    ## selecao do algoritmo de classificacao
    while(True):
        try:
            select_algoritmo = int(raw_input('Modo do k-nn:\n[1] k-NN\n[2] k-NN ponderado\n>>'))-1
            if select_algoritmo in [0,1] == False:
                raise ValueError
            break
        
        except ValueError: print ('\nOpcao invalida\n')            

    ## selecao da metrica de distancia
    while(True):
        try:
            select_distancia = int(raw_input('Distancia:\n[1] Euclidiana\n[2] HVDM\n[3] VDM\n>>'))-1
            if select_distancia in [0,1,2] == False:
                raise ValueError
            if select_distancia == 1 or select_distancia == 2:
                q = int(raw_input('Valor de q\n>> '))
            break
        
        except ValueError: print ('\nOpcao invalida\n')

    for kf in range(len(lista_kf)):
        
        k_fold = int(lista_kf[kf])
        
        for kn in range(len(lista_k)):

            k = int(lista_k[kn])

            resultado_taxas = []
            tempo_execucao = []
            
            for teste_atual in range(qtd_testes):
                ## abrir arquivo e acessar dados
                a = arquivo()
                a.abrir(nome_arquivo)

                atributos, classes = a.get_dataset(k_fold)
                
                taxas_acertos = []
                tempo_conjunto = []
                for n_conj in range(len(atributos)):
                    conjunto_teste = atributos[0]
                    classe_teste = classes[0]
                    
                    atributos.remove(conjunto_teste)
                    classes.remove(classe_teste)

                    conjunto_treino = []
                    for i in range(len(atributos)):
                        for j in range(len(atributos[i])):
                            conjunto_treino.append(atributos[i][j])

                    classe_treino = []
                    for i in range(len(classes)):
                        for j in range(len(classes[i])):
                            classe_treino.append(classes[i][j])
                
                    ## knn
                    if select_algoritmo == 0:
                        predicoes, tempo = calcula_knn(conjunto_treino, classe_treino, conjunto_teste, k, modo_distancia[select_distancia], q)
                        taxa_acerto = calcular_accuracia(predicoes, classe_teste)

                    ## knn ponderado
                    elif select_algoritmo == 1:
                        predicoes,tempo = calcula_knn(conjunto_treino, classe_treino, conjunto_teste, lista_k, modo_distancia[select_distancia], q,True)
                        taxa_acerto = calcular_accuracia(predicoes, classe_teste)

                    taxas_acertos.append(taxa_acerto)
                    tempo_conjunto.append(tempo)
                    
                    atributos.append(conjunto_teste)
                    classes.append(classe_teste)

                resultado_taxas.append(taxas_acertos)
                tempo_execucao.append(tempo_conjunto)
                
            medias_conjunto = []
            for i in range(len(resultado_taxas)):
                m = 0
                qtd = len(resultado_taxas[i])
                for j in range(len(resultado_taxas[i])):
                    m  += resultado_taxas[i][j]
                    
                m = m/qtd
                medias_conjunto.append(m)

            media_total = 0
            for media in medias_conjunto:
                media_total += media

            qtd = len(medias_conjunto)
            media_total = media_total/qtd

            media_tempo = []
            for i in range(len(tempo_execucao)):
                m = 0
                qtd = len(tempo_execucao[i])
                for j in range(len(tempo_execucao[i])):
                    m += tempo_execucao[i][j]
                media_tempo.append(m)

            media_t_total = 0
            for m in media_tempo:
                media_t_total += m

            media_t_total = media_t_total/len(media_tempo)
            
##            print ('Numero de vizinhos (Kn): '+str(k))
##            print ('Numero de conjuntos (Kf): '+str(k_fold))
##            print ('Taxa de acerto media\t|\tTempo medio de execucao')
            print (str(round(media_total,3))+'\t|\t'+str(round(media_t_total,3))+' s')

        print('__________________________________________________________')

    resp = raw_input("Encerrar S/N? ").upper()
    r_exit = 'S' != resp
