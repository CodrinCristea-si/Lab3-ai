# define the function
import math
import numpy as np
from random import randint
# define a generator of values
import os
from random import uniform, randint, seed
from utils import *
from BinChromosome import *
from GeneticAlgorithm import *
#  plot the 1D function (n = 1) (see how the search space looks)
import matplotlib.pyplot as plt
"""
Aceasta functie determinam comunitatile dintr-o retea
network este o retea
Returneaza cel mai bun cromozome din retea 
"""
def communities(network):
    bestsofar = None
    # initialise de GA parameters
    gaParam = {'popSize': 50, 'noGen': 100}
    # problem parameters
    problParam = {'function': noConexComp, 'noBits': network['noEdges'], 'network': network}

    generations = []

    ga = GA(gaParam, problParam)
    ga.initialisation()
    ga.evaluation()

    max = 0
    for g in range(gaParam['noGen']):
        # plotting preparation
        generations.append(g)
        # logic alg
        ga.oneGeneration()
        # ga.oneGenerationElitism()
        # ga.oneGenerationSteadyState()

        bestChromo = ga.bestChromosome()
        if bestChromo.fitness > max:
            max=bestChromo.fitness
            bestsofar=bestChromo

    return bestsofar

def chromo_to_comm(bestChromo,network):
    network['mat'] = bestChromo.repres
    comp_con = getConexComp(bestChromo.repres, bestChromo.fitness)
    network['communities'] = comp_con
    communitie = [0 for node in range(network['noNodes'])]
    index = 1
    for community in sorted(map(sorted, comp_con)):
        for node in community:
            communitie[node] = index
        index += 1
    return communitie
"""
Fucntia main
"""
def main():
    crtDir = os.getcwd()
    filePath1 = os.path.join(crtDir, 'data\\real\\dolphins', 'dolphins.gml')
    filePath2 = os.path.join(crtDir, 'data\\real\\football', 'football.gml')
    filePath3 = os.path.join(crtDir, 'data\\real\\karate', 'karate.gml')
    filePath4 = os.path.join(crtDir, 'data\\real\\krebs', 'krebs.gml')
    filePath5 = os.path.join(crtDir, 'graf_test_1.gml')
    filePath6 = os.path.join(crtDir, 'graf_test_2.gml')
    filePath7 = os.path.join(crtDir, 'graf_test_3.gml')
    filePath8 = os.path.join(crtDir, 'graf_test_6.gml')
    filePath9 = os.path.join(crtDir, 'graf_test_5.gml')
    filePath10 = os.path.join(crtDir, 'map.gml')
    network1 = readGML(filePath1)
    network2 = readGML(filePath2)
    network3 = readGML(filePath3)
    network4 = readGML(filePath4)
    network5 = readGML(filePath5)
    network6 = readGML(filePath6)
    network7 = readGML(filePath7)
    network8 = readGML(filePath8)
    network9 = readGML(filePath9)
    network10 = readGML(filePath10)

    bestChromo = communities(network1)
    communitie= chromo_to_comm(bestChromo,network1)
    plotNetwork(network1,"dolphins.gml", communitie)
    printCommunities(network1,"dolphins.gml")
    print("\n\n")

    bestChromo = communities(network2)
    communitie= chromo_to_comm(bestChromo,network2)
    plotNetwork(network2,"football.gml", communitie)
    printCommunities(network2,"football.gml")
    print("\n\n")

    bestChromo = communities(network3)
    communitie = chromo_to_comm(bestChromo, network3)
    plotNetwork(network3,"karate.gml", communitie)
    printCommunities(network3,"karate.gml")
    print("\n\n")

    bestChromo = communities(network4)
    communitie = chromo_to_comm(bestChromo, network4)
    plotNetwork(network4,"krebs.gml", communitie)
    printCommunities(network4,"krebs.gml")
    print("\n\n")

    bestChromo = communities(network5)
    communitie = chromo_to_comm(bestChromo, network5)
    plotNetwork(network5,"graf_test_1.gml", communitie)
    printCommunities(network5,"graf_test_1.gml")
    print("\n\n")

    bestChromo = communities(network6)
    communitie = chromo_to_comm(bestChromo, network6)
    plotNetwork(network6,"graf_test_2.gml", communitie)
    printCommunities(network6,"graf_test_2.gml")
    print("\n\n")

    bestChromo = communities(network7)
    communitie = chromo_to_comm(bestChromo, network7)
    plotNetwork(network7,"graf_test_3.gml", communitie)
    printCommunities(network7,"graf_test_3.gml")
    print("\n\n")

    bestChromo = communities(network8)
    communitie = chromo_to_comm(bestChromo, network8)
    plotNetwork(network8,"graf_test_5.gml", communitie)
    printCommunities(network8,"graf_test_5.gml")
    print("\n\n")

    bestChromo = communities(network9)
    communitie = chromo_to_comm(bestChromo, network9)
    plotNetwork(network9,"graf_test_6.gml", communitie)
    printCommunities(network9,"graf_test_6.gml")
    print("\n\n")

    bestChromo = communities(network10)
    communitie = chromo_to_comm(bestChromo, network10)
    plotNetwork(network10,"map.gml", communitie)
    printCommunities(network10,"map.gml")
    print("\n\n")


main()




