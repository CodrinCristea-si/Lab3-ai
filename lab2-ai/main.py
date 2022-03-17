# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import warnings
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

warnings.simplefilter('ignore')
"""
Functie pycharm IDE
"""
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

"""
Citeste datele unui graf dintr-un fisier txt
fileName- numele fisierului
Returneaza un dictionar network net care contine
net['noNodes'] - numarul de noduri
net['noEdges'] - numarul de muchii
net['mat'] - matricea de adiacenta
net['degrees'] - o lista cu gradele fiecarui nod
"""
# read the network details
def readNet(fileName):
    f = open(fileName, "r")
    net = {}
    n = int(f.readline())
    net['noNodes'] = n
    mat = []
    for i in range(n):
        mat.append([])
        line = f.readline()
        elems = line.split(" ")
        for j in range(n):
            mat[-1].append(int(elems[j]))
    net["mat"] = mat
    degrees = []
    noEdges = 0
    for i in range(n):
        d = 0
        for j in range(n):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    net["noEdges"] = noEdges
    net["degrees"] = degrees
    f.close()
    return net

"""
Citeste datele unui graf dintr-un fisier gml
fileName- numele fisierului
Returneaza o retea care este un dictionar network net care contine
net['noNodes'] - numarul de noduri
net['noEdges'] - numarul de muchii
net['mat'] - matricea de adiacenta
net['degrees'] - o lista cu gradele fiecarui nod
 net['dict_id'] - un dictionar ce contine label-ul sau denumirea nodului si numarul care ii este asignat
"""
def readGML(fileName):
    net = {}
    noNodes = 0
    noEdges = 0
    initi = False
    mat = []
    dict_id = {}
    with open(fileName,'r') as f:
        line = f.readline()
        while line != "":
            line = line.strip() # eliminam spatiile libere
            if line == "node":
                noNodes += 1
                f.readline()# trecem peste [
                id = f.readline().strip().split(" ")[1]
                dict_id[id] = noNodes-1
            elif line == "edge":
                # trebuie sa trecem de toate nodurile ca sa ajungem la muchii
                # dupa ce citim toate nodurile stim dimensiunile matricei de adiacenta
                # iar daca e prima muchie mai intai initializam matricea de adiacenta
                if initi == False:
                    mat = init_mat(noNodes)
                    initi = True
                f.readline() # trecem peste [
                x = f.readline().strip().split(" ")[1]  # linia cu source
                y = f.readline().strip().split(" ")[1] # linia cu  target
                # salvam muchia in matricea de adiacenta
                mat[dict_id[x]][dict_id[y]] = mat[dict_id[y]][dict_id[x]] = 1
            line = f.readline()
    #calculam gradele fiecarui nod
    degrees = []
    for i in range(noNodes):
        d = 0
        for j in range(noNodes):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    # salvam datele intr-un dictionar
    net['noNodes'] = noNodes
    net['noEdges'] = noEdges
    net['mat'] = mat
    net['dict_id'] = dict_id
    net['degrees'] = degrees
    return net


"""
Afiseaza un plot
network - reteaua ce trebuie afisata
Nu are parametri 
"""
# plot a network
def plotNetwork(network, communities = []):
    if communities != []:
        comunities = [1 for node in range(network["noNodes"])]
    np.random.seed(123) #to freeze the graph's view (networks uses a random view)
    A=np.matrix(network["mat"])

    G=nx.from_numpy_matrix(A)

    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(4, 4))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color = communities)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()
"""
Aceasta functie este o replia a algoritmului girvan-newman pe baza aceluiasi algoritm
network - o retea (cea din citire)
Returneaza un tuple de set-uri, fiecare set reprezinta o componenta conexe
"""
def girvan_newman_remastered(network):
    components = [] # lista de componente conexe
    init_nr_comp = noConexComp(network) # nr initial de componente conexe
    init_no_edges = network['noEdges'] # numarul initial de noduri
    current_nr_comp = init_nr_comp # nr curent de componente conexe
    current_no_edges = 0 # nr curent de muchii
    # se ruleaza algoritmul cat timp s-a sters o muchie si cat timp nu a crescut nr-ul de componente conexe
    # adica cat timp n-am descoperit o noua societate
    while current_no_edges != init_no_edges and current_nr_comp <= init_nr_comp:
        #print("cur much", current_no_edges)
        #print("cur comp", current_nr_comp)
        A = np.matrix(network["mat"])
        # conversie catre graful din numpy pt a calcula edge_betweenness_centrality
        G = nx.from_numpy_matrix(A)
        betweenness = nx.edge_betweenness_centrality(G)
        # calculam muchia cu edge_betweenness_centrality maxim
        edge = max_value_betweenness_edge(betweenness)
        # eliminam muchia
        network["mat"][edge[0]][edge[1]] = network["mat"][edge[1]][edge[0]] = 0
        network['noEdges'] -= 1
        # reactualizam datele
        init_no_edges = current_no_edges
        current_nr_comp = noConexComp(network)
        current_no_edges = network['noEdges']
    # determinam componentele conexe si returnam
    components = tuple(getConexComp(network, current_nr_comp))
    return components
"""
Determina numarul de componente conexe dintr-un graf
network- o retea
Returneaza un int cu semnificatia de mai sus
"""
def noConexComp(network):
    nr = 0 # nr de comp conexe
    viz = [0 for i in range(network["noNodes"])] # vectorul de vizite, atunci cand un nod e vizitat, pe pozitia lui se pune 1
    suma = 0
    for i in range(network["noNodes"]):
        dfs(network["mat"],viz,i,1)
        # daca suma din viz e diferita de cea anterioara inseamna ca am gasit o noua componenta conexa
        sumInt = sum(viz)
        if sumInt > suma :
            nr += 1
        suma = sumInt
    return nr

"""
Algoritmul dfs folosit pt impadurirea/descoperirea unei componente conexe
mat- atricea de adiacenta
viz- o lista de elemente care semnifica daca un nod a fost vizitat sau nu
node - nodul de la care se incepe descoperirea
val - valoarea pe care o pune in viz atunci cand descopera un alt nod
"""
def dfs(mat,viz,node,val):
    #daca nodul e nevizitat incepem explorarea
    if viz[node] == 0:
        viz[node] = val
        for i in range(len(mat[node])):
            #cautam vecini neexplorati
            if mat[node][i] == 1 and viz[i] == 0:
                dfs(mat,viz,i,val)

"""
Calzuleaza maximul valorii unui dictionar
dict - un dictionar de valori
returneaza valoarea maxima din dict
"""
def max_value_betweenness_edge(dict):
    max = -1e9
    edge = 0
    # parcurgem lista de muchii si vedeam care are valoarea cea mai mare
    for el in dict:
        if dict[el] > max:
            max = dict[el]
            edge = el
    return edge

"""
Determina componentele conexe dintr-n graf stiind numarul acestora
network - o retea
nr_conex_comp - nr de componente conexe din network
Returneaza un tuple de set-uri, fiecare set reprezinta o componenta conexe
"""
def getConexComp(network,nr_conex_comp):
    nr = 0 # nr comp coenxe
    viz = [0 for i in range(network["noNodes"])]# vectorul de vizite, atunci cand un nod e vizitat, pe pozitia lui se pune 1
    suma = 0
    val = 1
    for i in range(network["noNodes"]):
        dfs(network["mat"], viz, i,val)
        sumInt = sum(viz)
        # daca suma din viz e diferita de cea anterioara inseamna ca am gasit o noua componenta conexa si trebuie sa-i dam o alta codificare
        if sumInt > suma:
            val += 1
        suma = sumInt

    # vom salva fiecare componenta intr-o lista
    comp_con = []
    for nr_comp in range(1,nr_conex_comp+1):
        list = []
        # determinam o componenta
        for i in range(network['noNodes']):
            if viz[i] == nr_comp:
                list.append(i)
        comp_con.append(set(list))
    return comp_con

"""
Aceasta functie determina numarul de comunitati dintr-un graf
network - o retea
returneaza o lista
Returneaza o lista de aceeasi dimensiune ca si reteaua, doar ca fiecarui nod ii este asignat o valoare(o societate)
"""
def greedyCommunitiesDetectionByTool(network):
    # Input: a graph
    # Output: list of comunity index (for every node)

    from networkx.algorithms import community

    A=np.matrix(network["mat"])
    G=nx.from_numpy_matrix(A)
    communities_generator = community.girvan_newman(G)
    top_level_communities = next(communities_generator)

    sorted(map(sorted, top_level_communities))
    network['communities'] = top_level_communities
    communities = [0 for node in range(network['noNodes'])]

    index = 1
    for community in sorted(map(sorted, top_level_communities)):
        for node in community:
            communities[node] = index
        index += 1
    return communities
# Press the green button in the gutter to run the script.

"""
Aceasta functie determina numarul de comunitati dintr-un graf
network - o retea
Returneaza o lista de aceeasi dimensiune ca si reteaua, doar ca fiecarui nod ii este asignat o valoare(o societate)
"""
def greedyCommunitiesDetection(network):
    # Input: a graph
    # Output: list of comunity index (for every node)

    # determinam comunitatile
    communities_generator = girvan_newman_remastered(network)
    sorted(map(sorted, communities_generator))
    network['communities'] = communities_generator

    # asignam pentru fiecare nod comunitatea din care face parte
    communities = [0 for node in range(network['noNodes'])]
    index = 1
    for community in sorted(map(sorted, communities_generator)):
        for node in community:
            communities[node] = index
        index += 1
    return communities

"""
Aceasta functie determina numarul de comunitati dintr-un graf
network - o retea
k - un int care reprezinta nr-ul de comunitati la care trebuie sa se ajung
Returneaza o lista de aceeasi dimensiune ca si reteaua, doar ca fiecarui nod ii este asignat o valoare(o societate)
"""
def greedyCommunitiesDetectionByK(network,k):
    # Input: a graph
    # Output: list of comunity index (for every node)

    # determinam comunitatile
    for i in range(k):
        communities_generator = girvan_newman_remastered(network)
    sorted(map(sorted, communities_generator))
    network['communities'] = communities_generator

    # asignam pentru fiecare nod comunitatea din care face parte
    communities = [0 for node in range(network['noNodes'])]
    index = 1
    for community in sorted(map(sorted, communities_generator)):
        for node in community:
            communities[node] = index
        index += 1
    return communities
"""
Testul comparare rezultate intre replica girvan-newman si cel buit-in pt reteaua de delfini
Nu are parametri
Nu returneaza nimic
AssertionError daca pica testele
"""
def testDolf():
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data\\real\\dolphins', 'dolphins.gml')
    network = readGML(filePath)
    rez1 = greedyCommunitiesDetectionByTool(network)
    rez2 = greedyCommunitiesDetection(network)
    assert (len(rez1) == len(rez2))
    assert (rez1 == rez2)

"""
Testul comparare rezultate intre replica girvan-newman si cel buit-in pt reteaua de football
Nu are parametri
Nu returneaza nimic
AssertionError daca pica testele
"""
def testFot():
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data\\real\\football', 'football.gml')
    network = readGML(filePath)
    rez1 = greedyCommunitiesDetectionByTool(network)
    rez2 = greedyCommunitiesDetection(network)
    assert (len(rez1) == len(rez2))
    assert (rez1 == rez2)

"""
Testul comparare rezultate intre replica girvan-newman si cel buit-in pt reteaua de karate
Nu are parametri
Nu returneaza nimic
AssertionError daca pica testele
"""
def testKar():
        crtDir = os.getcwd()
        filePath = os.path.join(crtDir, 'data\\real\\karate', 'karate.gml')
        network = readGML(filePath)
        rez1 = greedyCommunitiesDetectionByTool(network)
        rez2 = greedyCommunitiesDetection(network)
        assert (len(rez1) == len(rez2))
        assert (rez1 == rez2)

"""
Testul comparare rezultate intre replica girvan-newman si cel buit-in pt reteaua de krebs
Nu are parametri
Nu returneaza nimic
AssertionError daca pica testele
"""
def testKreb():
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data\\real\\krebs', 'krebs.gml')
    network = readGML(filePath)
    rez1 = greedyCommunitiesDetectionByTool(network)
    rez2 = greedyCommunitiesDetection(network)
    assert (len(rez1) == len(rez2))
    assert (rez1 == rez2)

"""
Testul comparare performanta si rezultate intre replica girvan-newman si cel buit-in pt reteaua de delfini
Nu are parametri
Nu returneaza nimic
AssertionError daca pica testele
"""
def testHighComplexity():
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data\\real\\dolphins', 'dolphins.gml')
    network = readGML(filePath)
    A = np.matrix(network["mat"])
    G = nx.from_numpy_matrix(A)
    communities_generator = community.girvan_newman(G)
    for i in range(1,4):
        top_level_communities = next(communities_generator)
        communities_generator_mast = girvan_newman_remastered(network)
        sorted(map(sorted, top_level_communities))
        assert(top_level_communities == communities_generator_mast)

"""
Un test care ruleaza toate testele
Nu are parametri
Nu returneaza nimic
"""
def testAll():
    testDolf()
    testFot()
    testKar()
    testKreb()
    testHighComplexity()


"""
Afiseaza comunitatile gasita in retea
network - o retea
Nu returneaza nimic
"""
def printCommunities(network):
    print("Sunt",network['noNodes'], "membri in graf")
    print("Sunt",len(network['communities']), "comunitati active gasite pana acum")
    com = 1
    for community in network['communities']:
        print("Comunitatea",com,"este formata din nodurile",community)
        com += 1


# partea de main
if __name__ == '__main__':
    print_hi('PyCharm')
    print("Incarcare teste")
    testAll()
    print("Teste finalizate cu succes")
    # load a network
    crtDir = os.getcwd()
    #filePath1 = os.path.join(crtDir, 'data', 'net.in')
    filePath2 = os.path.join(crtDir, 'data\\real\\dolphins', 'dolphins.gml')
    filePath3 = os.path.join(crtDir, 'data\\real\\football', 'football.gml')
    filePath4 = os.path.join(crtDir, 'data\\real\\karate', 'karate.gml')
    filePath5 = os.path.join(crtDir, 'data\\real\\krebs', 'krebs.gml')
    filePath6 = os.path.join(crtDir,  'graf_test_1.gml')
    filePath7 = os.path.join(crtDir, 'graf_test_2.gml')
    filePath8 = os.path.join(crtDir, 'graf_test_3.gml')
    filePath9 = os.path.join(crtDir, 'graf_test_6.gml')
    filePath10 = os.path.join(crtDir, 'graf_test_5.gml')
    #filePath= input("Introduceti calea absoluta a fisierului: ")
#    print("Calea este",filePath)
    network2 = readGML(filePath2)
    network3 = readGML(filePath3)
    network4 = readGML(filePath4)
    network5 = readGML(filePath5)
    network6 = readGML(filePath6)
    network7 = readGML(filePath7)
    network8 = readGML(filePath8)
    network9 = readGML(filePath9)
    network10 = readGML(filePath10)
    #print("Nr-ul de legaturi este",network['noEdges'])
    # plot the network
   # plotNetwork(network)
    # plot a particular (mock) division in communities
    #mockCommunities = [1, 2, 1, 2, 1, 1]
    #plotNetwork(network, mockCommunities)
    #plotNetwork(network, greedyCommunitiesDetectionByTool(network))
    print("dolphins")
    plotNetwork(network2, greedyCommunitiesDetectionByK(network2,12))
    printCommunities(network2)
    print("football")
    plotNetwork(network3, greedyCommunitiesDetectionByK(network3, 12))
    printCommunities(network3)
    print("karate")
    plotNetwork(network4, greedyCommunitiesDetectionByK(network4, 12))
    printCommunities(network4)
    print("krebs")
    plotNetwork(network5, greedyCommunitiesDetectionByK(network5, 12))
    printCommunities(network5)
    print("graf_test_1")
    plotNetwork(network6, greedyCommunitiesDetectionByK(network6, 12))
    printCommunities(network6)
    print("graf_test_2")
    plotNetwork(network7, greedyCommunitiesDetectionByK(network7, 12))
    printCommunities(network7)
    print("graf_test_3")
    plotNetwork(network8, greedyCommunitiesDetectionByK(network8, 12))
    printCommunities(network8)
    print("graf_test_6")
    plotNetwork(network9, greedyCommunitiesDetectionByK(network9, 12))
    printCommunities(network9)
    print("graf_test_5")
    plotNetwork(network10, greedyCommunitiesDetectionByK(network10, 12))
    printCommunities(network10)



