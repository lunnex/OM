import math
import random
import struct

import numpy as np

class Inhabitant:
    def __init__(self, x):
        self.edges = x
        self.chance = 0


visited_nodes = []


def is_circle(branch, max_power):
    if visited_nodes.count(branch[0]) > max_power - 1 or visited_nodes.count(branch[1]) > max_power - 1:
        return True

    if branch[0] in visited_nodes and branch[1] in visited_nodes:
        return True

    return False


def is_adjacent(edge, num_of_iteration):
    if num_of_iteration == 0:
        fill_visited_nodes(edge)
        return True

    if edge[0] not in visited_nodes and edge[1] not in visited_nodes:
        return False

    fill_visited_nodes(edge)
    return True


def is_already_contains_edge(tree, edge):
    if (edge[1], edge[0]) in tree:
        return True
    return False


def fill_visited_nodes(edge):
    for node in edge:
        visited_nodes.append(node)


def is_full_tree(tree, matrix_size):
    if len(tree) < matrix_size - 1:
        return False
    else:
        return True


def func (x):
    return math.sin((5/2) * math.cos(x))
    #return x

def bin2float(b):
    h = int(b, 2).to_bytes(8, byteorder="big")
    return struct.unpack('>d', h)[0]

def float2bin(f):
    [d] = struct.unpack(">Q", struct.pack(">d", f))
    return f'{d:064b}'

def setMutation(m1, rndR1):
    m1List = list(m1)
    if(m1[rndR1] == 0):
        m1List[rndR1] = '1'
        m1 = ''.join(m1List)
    else:
        m1List[rndR1] = '0'
        m1 = ''.join(m1List)
    return m1

def printGeneration(arr):
    ys = []
    xs = []
    chances = []
    maxVal = 0
    numOfMax = 0
    for i in range(0, len(arr)):
        ys.append(arr[i].y)
        xs.append(arr[i].x)
        chances.append(arr[i].chance)
        if(maxVal < arr[i].chance):
            maxVal = arr[i].chance
            numOfMax = i
    print("Средние значения в поколении")
    print(np.average(xs), np.average(ys), np.average(chances))
    print("Особь с наибольшим значением функциии полезности")
    print(arr[numOfMax].x, arr[numOfMax].y, arr[numOfMax].chance)
    print("________________________________________________________________")


sizeOfGeneration = 5
countOfIterations = 10
inhabitants = []
mutationThreshold = 1000

#Область поиска минимума функции
a = 1
b = 50

g = [[0, 5, 6, 7, 8, 9],
     [5, 0, 1, 2, 3, 4],
     [6, 1, 0, 9, 8, 7],
     [7, 2, 9, 0, 6, 5],
     [8, 3, 8, 6, 0, 4],
     [9, 4, 7, 5, 4, 0]]

#Порождаем перую популяцию
for i in range(0, sizeOfGeneration):
    edges = []
    j = 0
    while len(edges) < len(g) - 1:
        newEdge = (random.randrange(0, len(g)), random.randrange(0, len(g)))
        if not is_already_contains_edge(edges, newEdge) and not is_circle(newEdge, 2):
            edges.append((random.randrange(0, len(g)), random.randrange(0, len(g))))
            j += 1
    visited_nodes.clear()
    inhabitants.insert(i, Inhabitant(edges))

#Считаем относительный вес
def SetWeight(arr):
    for i in range(0, len(arr)):
        weight = 0
        for edge in arr[i].edges:
            weight += g[edge[0]][edge[1]]

        arr[i].chance = weight

SetWeight(inhabitants)

#Создание нового поколения
newGeneration = []



def TournamentSelection():
    global aliveNewGeneration

    tournamentOrder = random.sample(range(len(newGeneration)), len(newGeneration))
    i = 0

    while (len(aliveNewGeneration) < len(inhabitants)):
        if (newGeneration[tournamentOrder[i]].chance > newGeneration[tournamentOrder[i + 1]].chance):
            aliveNewGeneration.append(newGeneration[tournamentOrder[i]])
        else:
            aliveNewGeneration.append(newGeneration[tournamentOrder[i + 1]])
        i += 2


    #print(distribution)

def OnePointCrossover():
    cut = random.randrange(60, 63)
    numOfEdge = random.randrange(0, len(g) - 1)
    leftOrRight = random.randrange(0, 1)

    b1 = float2bin(pair[0].edges[numOfEdge][leftOrRight])
    b1cut1 = b1[0:cut]
    b1cut2 = b1[cut:64]

    b2 = float2bin(pair[1].edges[numOfEdge][leftOrRight])
    b2cut1 = b2[0:cut]
    b2cut2 = b2[cut:64]

    ch1 = b1cut1 + b2cut2
    ch2 = b2cut1 + b1cut2



    # Мутация
    if (random.randrange(0, 1000) > mutationThreshold):
        rndR1 = random.randrange(30, len(ch1))
        ch1 = setMutation(ch1, rndR1)

        rndR2 = random.randrange(30, len(ch2))
        ch2 = setMutation(ch2, rndR2)


    edge0 = list(pair[0].edges[numOfEdge])
    edge1 = list(pair[1].edges[numOfEdge])

    edge0[leftOrRight] = bin2float(ch1)
    edge1[leftOrRight] = bin2float(ch2)

    pair[0].edges[numOfEdge] = edge0
    pair[1].edges[numOfEdge] = edge1



   # newGeneration.append(e)
    newGeneration.append(pair[1].edges[numOfEdge][leftOrRight])





for r in range(0, countOfIterations):
    while(len(newGeneration) < len(inhabitants) * 2):
        pair = []
        while len(pair) < 2:
            #Случайным образом получаем особь
            rndNum = random.randrange(0, len(inhabitants))
            pair.append(inhabitants[rndNum])

        OnePointCrossover()

    aliveNewGeneration = []
    SetWeight(newGeneration)

    TournamentSelection()

    # Дорогу молодым
    try:
        for i in range(0, len(inhabitants)):
            inhabitants[i] = aliveNewGeneration[i]
    except:
        print(len(aliveNewGeneration))

    newGeneration = []

    #Расчет функции полезности для нового поколения
    SetWeight(inhabitants)

    printGeneration(aliveNewGeneration)



