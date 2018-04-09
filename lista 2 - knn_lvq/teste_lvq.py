from lvq1 import lvq1

database = [[1, 2, 'a'], [1, 2, 'a'], [1, 2, 'a'], [0, 0, 'b'], [1, 2, 'b']]

lvq = lvq1()
lvq.config(database,3)
print lvq.get_prototipos()
