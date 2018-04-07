## UFPE - CIn
## Aprendizagem de Máquina
## Rebeca Paula Alves de Oliveira [rpao]
## Lista 1 - Resolução

1 - Na pasta 'data' estão os arquivos referentes as bases de dados utilizadas, todos no formato .csv, que é o padrão lido

2 - Para executar o programa é necessário: python 2.7 com as bibliotecas csv, numpy, math, operator, random e time

3 - Para executar o programa, é necessário compilar o arquivo main.py, os outros arquivos são classes utilizadas por ele

4 - Compilando o arquivo main.py:

4.1 - Das configurações realizadas pelo usuário:
	>> 'Informe caminho do arquivo: ' -> digite o caminho completo do arquivo, se for utilizar um dos arquivos existentes 
										 na pasta data, digite: data\<nome>.csv.
										 O arquivo deve ser no formato csv para evitar erros de execução, com os atributos
										 separados por vírgula.
	
	>> 'quantidade de testes: ' -> número de testes executados para cada possível configuração (Kn, Kf)
	
	>> 'Informe a quantidade de vizinhos ...' -> atribui valor a Kn e recebe apenas uma lista de inteiros positivos, 
												 com um ou mais inteiros separados por espaço (Sem espaço após o ultimo valor)
	
	>> 'Informe a quantidade de conjuntos...' -> atribui valor a Kf e recebe apenas uma lista de inteiros positivos, 
												 com um ou mais inteiros separados por espaço (Sem espaço após o ultimo valor)
	
	>> 'Modo do k-nn: ' -> se 1, executa k-nn, se 2 executa k-nn com pesos
	
	>> 'Distancia: ' -> se 1, executa com distância euclidiana, se 2, executa com distância hvdm e se 3, executa com 
						distância vdm

4.2 - Da saída:
	>>	imprime na tela o número de vizinhos (Kn), o número de conjuntos (Kf), taxas de acerto médias e tempo médio de 
		execução (em segundos) para cada combinação (Kn, Kf)
		
5 - Dos arquivos existentes na pasta principal:
	arquivo.py: classe responsável por abrir o arquivo, aleatorizar as instâncias e gerar os Kf conjuntos
	
	euclidiana.py: classe que possuí apenas uma função para calcular a distância euclidiana entre dois pontos
	
	hvdm.py: classe que executa o algoritmo de calculo de distâncias dos vizinhos utilizando a distância euclidiana para 
			 dados numéricos e a distância vdm para dados categóricos, retornando uma lista dos vizinhos com suas respectivas 
			 distâncias.
	
	k_nn.py: classe chamada pela main para executar cada um dos tipos de algoritmos, sendo eles k-nn ou k-nn com pesos, 
			 utilizando uma das possíveis distâncias
	
	main.py: arquivo principal que executa o programa implementado.
	
	value_difference_metric.py: classe que calcula a distância VDM entre duas instâncias
	
	vdm.py: classe que executa o algoritmo de calculo de distâncias dos vizinhos de uma entrada de acordo com a distância VDM, 
			retornando uma lista de vizinhos com suas respectivas distâncias