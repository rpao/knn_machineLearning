import math
import numpy as np

from value_difference_metric import value_difference_metric

class euclidiana(object):
    
    ## calcula a distancia euclidiana entre duas instancias
    def calcular(self, inst1, inst2, peso):
        d = 0
        for i in range(len(inst1)):
            if peso:
                try: d += 1.0/pow(abs(inst1[i]-inst2[i]), 4)
                except ZeroDivisionError: d += 0

            else: d += pow((inst1[i] - inst2[i]), 2)
            
        return math.sqrt(d)
