from random import randint
from utils import *


# Binary representation
class Chromosome:
    """
    Reprezentarea pentru acest cromozome:
    Dimensiunea reprezentarii este egala cu nr-ul de muchii din retea
    Este sub forma de lista, unde fiecare muchie ii este asignata o
    pozitie din lista, iar fiecare valoare din lista este ori 0 ori 1,
    unde 1 reprezinta faptul ca muchia asignata acelei pozitii este desenata, 0 altfel
    """
    def __init__(self, problParam=None):
        self.__problParam = problParam
        self.__repres = []
        for _ in range(self.__problParam['network']['noEdges']):
            val = randint(0, 1)
            self.__repres.append(val)
        self.__fitness = 0.0

    """
    Reprezentarea este sub forma unei matrici de adiacenta
    """
    @property
    def repres(self):
        # convert the binary matrix to a list of real values
        mat = init_mat(self.__problParam['network']['noNodes'])
        #print(len(mat))
        for edge in self.__problParam['network']['edge_id']:
            #print(edge)
            #print(self.__problParam['network']['edge_id'][edge],self.__problParam['network']['noEdges'])
            if self.__repres[self.__problParam['network']['edge_id'][edge]] == 1:
                mat[int(edge[0])-1][int(edge[1])-1] = 1
                mat[int(edge[1])-1][int(edge[0])-1] = 1
        return mat

    """
    Valoarea functie de fitness
    """
    @property
    def fitness(self):
        return self.__fitness

    """
    Asignarea unei reprezentari
    """
    @repres.setter
    def repres(self, l=[]):
        self.__repres = l

    """
        Asignarea unei valori pentru functie de fitness
        """
    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    """
    Incrucisarea printr-un sg pct de taietura
    """
    def crossover(self, c):
        noBits = self.__problParam['noBits']
        cuttingPoint = randint(0, noBits - 1)
        newGene = [self.__repres[i] if i < cuttingPoint else c.__repres[i] for i in range(noBits)]
        offspring = Chromosome(self.__problParam)
        offspring.repres = newGene
        return offspring

    """
    Mutatie tare - bit flipping
    """
    def mutation(self):
        bit = randint(0, len(self.__repres) - 1)
        self.__repres[bit] = 1 - self.__repres[bit]

    def __str__(self):
        return '\nChromo: ' + str(self.__repres) + ' has fit: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness
