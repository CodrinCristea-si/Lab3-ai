from random import uniform

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def generateNewValue(lim1, lim2):
    return uniform(lim1, lim2)

def binToInt(x):
    val = 0
    # x.reverse()
    for bit in x:
        val = val * 2 + bit
    return val

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
    edge_id = {}
    val_edge = 0
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
                if (int(x),int(y)) not in edge_id:
                    edge_id[(int(x),int(y))] = val_edge
                    val_edge += 1
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
    net['edge_id'] = edge_id
    net['degrees'] = degrees
    print('val', val_edge)
    return net

"""
Initializeaza o matrice de adiacenta de noNodes x noNodes
noNodes- dimensiunea matricei
Returneaza o matricea cu dimensiunea de mai sus, plina cu valori de 0
"""
def init_mat(noNodes):
    mat = []
    for i in range(noNodes):
        #adaugam cate o linie noua si goala
        mat.append([])
        for j in range(noNodes):
            #adaugam cate un 0 in fiecare linie
            mat[i].append(0)
    return mat

"""
Determina numarul de componente conexe dintr-un graf
network- o retea
Returneaza un int cu semnificatia de mai sus
"""
def noConexComp(mat):
    nr = 0 # nr de comp conexe
    viz = [0 for i in range(len(mat))] # vectorul de vizite, atunci cand un nod e vizitat, pe pozitia lui se pune 1
    suma = 0
    for i in range(len(mat)):
        dfs(mat,viz,i,1)
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
Determina componentele conexe dintr-n graf stiind numarul acestora
network - o retea
nr_conex_comp - nr de componente conexe din network
Returneaza un tuple de set-uri, fiecare set reprezinta o componenta conexe
"""
def getConexComp(mat,nr_conex_comp):
    nr = 0 # nr comp coenxe
    viz = [0 for i in range(len(mat))]# vectorul de vizite, atunci cand un nod e vizitat, pe pozitia lui se pune 1
    suma = 0
    val = 1
    for i in range(len(mat)):
        dfs(mat, viz, i,val)
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
        for i in range(len(mat)):
            if viz[i] == nr_comp:
                list.append(i)
        comp_con.append(set(list))
    return comp_con

def readGML(fileName):
    net = {}
    noNodes = 0
    noEdges = 0
    initi = False
    mat = []
    dict_id = {}
    val_edge = 0
    edge_id = {}
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
                y = f.readline().strip().split(" ")[1] # linia cu target
                # salvam muchia in matricea de adiacenta
                mat[dict_id[x]][dict_id[y]] = mat[dict_id[y]][dict_id[x]] = 1
                if (x,y) not in edge_id and (y,x) not in edge_id:
                    edge_id[(x,y)] = val_edge
                    val_edge += 1
                    noEdges += 1
            line = f.readline()
    #calculam gradele fiecarui nod
    degrees = []
    for i in range(noNodes):
        d = 0
        for j in range(noNodes):
            if (mat[i][j] == 1):
                d += 1
            #if (j > i):
            #    noEdges += mat[i][j]
        degrees.append(d)
    # salvam datele intr-un dictionar
    net['noNodes'] = noNodes
    net['noEdges'] = noEdges
    net['mat'] = mat
    net['node_id'] = dict_id
    net['edge_id'] = edge_id
    net['degrees'] = degrees
    return net

"""
Afiseaza un plot
network - reteaua ce trebuie afisata
filename- numele fisierului caruia i se face plot
Nu returneaza nimic 
"""
# plot a network
def plotNetwork(network,filename, communities = []):
    if communities != []:
        comunities = [1 for node in range(network["noNodes"])]
    np.random.seed(123) #to freeze the graph's view (networks uses a random view)
    A = np.matrix(network["mat"])

    G = nx.from_numpy_matrix(A)

    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(4, 4))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color = communities)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.title(filename)
    plt.show()

"""
Afiseaza comunitatile gasita in retea
network - o retea
filename- numele fisierului caruia i se face plot
Nu returneaza nimic
"""
def printCommunities(network,filename):
    print("Pentru",filename)
    print("Sunt",network['noEdges'], "legaturi")
    print("Sunt",network['noNodes'], "membri in graf")
    print("Sunt",len(network['communities']), "comunitati active gasite pana acum")
    com = 1
    for community in network['communities']:
        print("Comunitatea",com,"este formata din nodurile",community)
        com += 1