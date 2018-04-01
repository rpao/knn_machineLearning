import time
import matplotlib.pyplot as plt

from lib_relatorio import lib_relatorio
from arquivo import arquivo
from k_nn import k_nn

tempo_treinamento = 0
tempo_classificacao = []

def plot_grafico (taxa_acertos, k, titulo):
    plt.figure(0)
    plt.plot(k, taxa_acertos, k, taxa_acertos, 'g^')
    plt.xlabel('valor de K')
    plt.ylabel('Acuracia')
    plt.title(titulo)
    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.grid(True)
    plt.show()

def calcular_accuracia(predicoes, cla_teste):
    ## acuracia de todos os testes realizados
    accuracias = []

    ## para cada k: taxas para seu conjunto de predicoes 
    for predicao in predicoes:
        acerto = 0

        ## calcula a quantidade de acertos
        for i in range(len(predicao)):
            if predicao[i] == cla_teste[i]: acerto += 1

        ## calcula a acuracia
        accuracia = acerto/float(len(cla_teste))
        
        accuracias.append(accuracia)

    return accuracias

def calcula_knn(conjunto_treino, classe_treino, conjunto_teste, lista_k = [1], distancia='Euclidiana', q=1, pesos=False):    
    knn = k_nn()
    
    tempo_treino = time.clock()
    
    knn.config(conjunto_treino, classe_treino, pesos, distancia, q)
    
    tempo_treinamento = time.clock() - tempo_treino
    
    ## vetor que guarda todas as predicoes realizadas na execucao
    predicoes = []
    
    for k in lista_k:
        start_time = time.clock()
        
        ## vetor que guarda todas as predicoes realizadas para k
        predicao = []

        ## obtem classe para cada instancia do conjunto de teste
        for entrada in conjunto_teste:
            classe_escolhida = knn.classificar(entrada, int(k))
            predicao.append(classe_escolhida)

        ## armazena no vetor de predicoes total
        predicoes.append(predicao)

        ## tempo de execucao do knn
        tempo_predicao = time.clock() - start_time
        tempo_classificacao.append(tempo_predicao)

    return predicoes          

modo_algoritmo = ['k-NN','k-NN ponderado']
modo_distancia = ['euclidiana', 'hvdm', 'vdm']

r_exit = True

while(r_exit):
    nome_arquivo = raw_input("Informe o caminho do arquivo:  ")
    
    qtd_testes = int(raw_input("quantidade de testes:  "))

    save_r = raw_input("Salvar relatorio(s) S/N?  ").upper()

    plot_r = raw_input("Gerar grafico(s) S/N?  ").upper()

    ## obtem valor(es) para k
    lista_k = raw_input("\nInforme quantidade de vizinhos\n!! Se mais de um, siga o exemplo: 1,2,3,... ou 1 2 3 ...\n>> ").replace(" ",",").split(",")

    while(True):
        try:
            k_fold = int(raw_input('\nInforme quantidade de conjuntos para o k-fold'))
            break        
        except: print ('\nOpcao invalida\n')
        
    while(True):
        try:
            select_algoritmo = int(raw_input('\nModo do k-nn:\n[1] k-NN\n[2] k-NN ponderado\n>>'))-1
            if select_algoritmo in [0,1] == False:
                raise NameError('Opcao invalida')

            break
        
        except: print ('\nOpcao invalida\n')
        
    while(True):
        try:
            select_distancia = int(raw_input('\nDistancia:\n[1] Euclidiana\n[2] HVDM\n[3] VDM\n>>'))-1
            if select_distancia in [0,1,2] == False:
                raise NameError('Opcao invalida')

            q = 1

            if select_distancia == 2 or select_distancia == 3:
                q = raw_input('\nValor de q (se 1, aperte Enter)\n>> ')
                if q == '': q = 1
                else: q = int(q)

            break
        
        except: print ('\nOpcao invalida\n')
    
    for teste_atual in range(qtd_testes):
        ## abrir arquivo e acessar dados
        a = arquivo()
        a.abrir(nome_arquivo)

        atributos, classes = a.get_dataset(k_fold)

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
                predicoes = calcula_knn(conjunto_treino, classe_treino, conjunto_teste, lista_k, modo_distancia[select_distancia], q)
                taxa_acerto = calcular_accuracia(predicoes, classe_teste)

            ## knn ponderado
            elif select_algoritmo == 1:
                predicoes = calcula_knn(conjunto_treino, classe_treino, conjunto_teste, lista_k, modo_distancia[select_distancia], q,True)
                taxa_acerto = calcular_accuracia(predicoes, classe_teste)

            ## relatorio
            relatorio = lib_relatorio()
            relatorio.set_arquivo(nome_arquivo,n_conj)
            relatorio.set_k(lista_k)
            relatorio.set_tamanho_conjunto(len(conjunto_treino),len(conjunto_teste))
            relatorio.set_modo(modo_algoritmo[select_algoritmo])
            relatorio.set_distancia(modo_distancia[select_distancia])
            relatorio.set_tempo(tempo_treinamento, tempo_classificacao)
            relatorio.set_taxa_acerto(taxa_acerto)
            relatorio.print_tela()
            if save_r == 'S':
                nome_relatorio = "relatorio_"+nome_arquivo.replace('.','_').replace('\\','_')+"_"+modo_algoritmo[select_algoritmo]+"_"+modo_distancia[select_distancia]+"_"+str(teste_atual)+".txt"
                relatorio.save(nome_relatorio)

            ## grafico
            if plot_r == 'S': plot_grafico (taxa_acerto, lista_k, 'Taxa de Acerto - k-NN')
                
            tempo_classificacao = []
            atributos.append(conjunto_teste)
            classes.append(classe_teste)

    resp = raw_input("Encerrar S/N? ").upper()
    r_exit = 'S' != resp
