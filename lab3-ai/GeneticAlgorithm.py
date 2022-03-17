from utils import binToInt, generateNewValue
from BinChromosome import *

class GA:
    def __init__(self, param=None, problParam=None):
        self.__param = param
        self.__problParam = problParam
        self.__population = []

    """
    Va retruna populatia/generatia curenta
    """
    @property
    def population(self):
        return self.__population

    """
    Popularea generatiei curente cu noi cromozomi
    """
    def initialisation(self):
        for _ in range(0, self.__param['popSize']):
            c = Chromosome(self.__problParam)
            self.__population.append(c)
    """
    Setarea valorii de fitness pentru fiecare cromozom
    """
    def evaluation(self):
        # de modificat
        for c in self.__population:
            c.fitness = self.__problParam['function'](c.repres)
    """
    Returneaza cel mai bun cromozom din populatia curenta
    """
    def bestChromosome(self):
        # de modificat
        best = self.__population[0]
        for c in self.__population:
            if c.fitness > best.fitness:
                best = c
        return best
    """
    Returneaza cel mai rau cromozome
    """
    def worstChromosome(self):
        # de modificat
        best = self.__population[0]
        for c in self.__population:
            if c.fitness < best.fitness:
                best = c
        return best
    """
    Selectie de tip turnir
    """
    def selection(self):
        pos1 = randint(0, self.__param['popSize'] - 1)
        pos2 = randint(0, self.__param['popSize'] - 1)
        if self.__population[pos1].fitness > self.__population[pos2].fitness:
            return pos1
        else:
            return pos2
    """
    Algoritm de generare a unei noi generatii cu inlocuirea totala a celei vechi
    """
    def oneGeneration(self):
        newPop = []
        for _ in range(self.__param['popSize']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    """
    Algoritm de generare a unei noi generatii cu inlocuirea totala a celei vechi 
    mai putin a celui mai bun cromozome
    """
    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()]
        for _ in range(self.__param['popSize'] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    """
    Algoritm de generare a unei noi generatii, in care la fiecare nou cromozom generat, se va inlocui cel mai rau cromozome din generatia curenta
    daca noul cromozome este mai bun
    """
    def oneGenerationSteadyState(self):
        for _ in range(self.__param['popSize']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            off.fitness = self.__problParam['function'](off.repres)
            worst = self.worstChromosome()
            if off.fitness > worst.fitness:
                worst = off