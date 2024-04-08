import math
import random
import struct

import numpy as np

class Inhabitant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.chance = 0

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

sizeOfGeneration = 100
inhabitants = []
mutationThreshold = 950

#Область поиска минимума функции
a = 1
b = 3

#Порождаем перую популяцию
for i in range(0, sizeOfGeneration):
    x = random.randrange(a * 1000, b * 1000) / 1000
    y = func(x)
    inhabitants.insert(i, Inhabitant(x, y))

#Считаем относительный вес
def SetWeight(arr):
    for i in range(0, len(arr)):
        #arr[i].chance = 1 - (inhabitants[i].y + 1) / 2
        arr[i].chance = arr[i].y * (-1)

SetWeight(inhabitants)

#Создание нового поколения
newGeneration = []


def OnePointCrossoverWithCopy():
    cut = random.randrange(0, 64)

    b1 = float2bin(pair[0].x)
    b1cut1 = b1[0:cut]
    b1cut2 = b1[cut:64]

    b2 = float2bin(pair[1].x)
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

    if (bin2float(ch1) >= a and bin2float(ch1) <= b):
        inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
        newGeneration.append(inhabitant)
    if (bin2float(ch2) >= a and bin2float(ch2) <= b):
        inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
        newGeneration.append(inhabitant)

def TournamentWithReturnSelection():
    global aliveNewGeneration

    while (len(aliveNewGeneration) <= len(inhabitants)):
        rndNum1 = random.randrange(0, len(newGeneration))
        rndNum2 = random.randrange(0, len(newGeneration))
        while (rndNum1 == rndNum2):
            rndNum2 = random.randrange(0, len(newGeneration))
        if (newGeneration[rndNum1].chance > newGeneration[rndNum2].chance):
            aliveNewGeneration.append(newGeneration[rndNum1])
        else:
            aliveNewGeneration.append(newGeneration[rndNum2])

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

def Proportional():
    global aliveNewGeneration

    distribution = {}

    sumchances = sum(inhabitant.chance for inhabitant in newGeneration)
    beginRange = 0
    endRange = 0
    for i in range(0, len(newGeneration)):
        relative = newGeneration[i].chance/sumchances
        endRange += relative
        distribution[(beginRange, endRange)] = newGeneration[i]
        beginRange += relative

    for i in range(0, len(inhabitants)):
        x = random.randrange(0,1000) / 1000

        for j in distribution:
            if(x > j[0] and x < j[1]):
                aliveNewGeneration.append(distribution[j])
                break

def Rank():
    global aliveNewGeneration
    newGeneration.sort(key=lambda inhabitant: inhabitant.chance, reverse=True)

    distributionRank = dict()
    for i in range(0, len(newGeneration)):
        if(i > 0 and newGeneration[i - 1].chance == newGeneration[i].chance):
            distributionRank[i-1] = newGeneration[i]
        else:
            distributionRank[i] = newGeneration[i]

    distribution = {}
    sumchances = sum(inhabitant.chance for inhabitant in newGeneration)
    beginRange = 0
    endRange = 0
    for i in distributionRank:
        relative = i / sumchances
        endRange += relative
        distribution[(beginRange, endRange)] = newGeneration[i]
        beginRange += relative

    for i in range(0, len(inhabitants)):
        x = random.randrange(0,1000) / 1000

        for j in distribution:
            if(x > j[0] and x < j[1]):
                aliveNewGeneration.append(distribution[j])
                break

    print(newGeneration)

    #print(distribution)

def StandartCrossover():
    b1 = float2bin(pair[0].x)
    s1 = b1[0]
    p11 = b1[1:6]
    p12 = b1[6:11]
    m11 = b1[11:38]
    m12 = b1[38:64]

    b2 = float2bin(pair[1].x)
    s2 = b2[0]
    p21 = b2[1:6]
    p22 = b2[6:11]
    m21 = b2[11:38]
    m22 = b2[38:64]

    ch1 = s1 + p11 + p22 + m11 + m22
    ch2 = s2 + p12 + p21 + m12 + m21

    if (random.randrange(0, 1000) > mutationThreshold):
        rndR1 = random.randrange(30, len(ch1))
        ch1 = setMutation(ch1, rndR1)

        rndR2 = random.randrange(30, len(ch2))
        ch2 = setMutation(ch2, rndR2)

    if (bin2float(ch1) >= a and bin2float(ch1) <= b):
        inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
        newGeneration.append(inhabitant)
    if (bin2float(ch2) >= a and bin2float(ch2) <= b):
        inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
        newGeneration.append(inhabitant)

def OnePointCrossover():
    cut = random.randrange(1, 63)

    b1 = float2bin(pair[0].x)
    b1cut1 = b1[0:cut]
    b1cut2 = b1[cut:64]

    b2 = float2bin(pair[1].x)
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

    if (bin2float(ch1) >= a and bin2float(ch1) <= b):
        inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
        newGeneration.append(inhabitant)
    if (bin2float(ch2) >= a and bin2float(ch2) <= b):
        inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
        newGeneration.append(inhabitant)

def TwoPointCrossover():
    cut1 = random.randrange(1, 63)
    cut2 = random.randrange(1, 63)

    b1 = float2bin(pair[0].x)
    b1cut1 = b1[0:cut1]
    b1cut2 = b1[cut1:cut2]
    b1cut3 = b1[cut2:64]

    b2 = float2bin(pair[1].x)
    b2cut1 = b2[0:cut1]
    b2cut2 = b2[cut1:cut2]
    b2cut3 = b2[cut2:64]

    ch1 = b1cut1 + b2cut2 + b1cut3
    ch2 = b2cut1 + b1cut2 + b2cut3

    # Мутация
    if (random.randrange(0, 1000) > mutationThreshold):
        rndR1 = random.randrange(30, len(ch1))
        ch1 = setMutation(ch1, rndR1)

        rndR2 = random.randrange(30, len(ch2))
        ch2 = setMutation(ch2, rndR2)

    try:
        if (bin2float(ch1) >= a and bin2float(ch1) <= b):
            inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
            newGeneration.append(inhabitant)
        if (bin2float(ch2) >= a and bin2float(ch2) <= b):
            inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
            newGeneration.append(inhabitant)
    except:
        pass

def EvenlyCrossover():
    b1 = float2bin(pair[0].x)
    b2 = float2bin(pair[1].x)
    ch1 = ""

    for i in range(0, 64):
        parent = random.randrange(0, 1)
        if parent == 0:
            ch1 += b1[i]
        else:
            ch1 += b2[i]

    ch2 = ""
    for i in range(0, 64):
        parent = random.randrange(0, 1)
        if parent == 0:
            ch2 += b1[i]
        else:
            ch2 += b2[i]

    if (random.randrange(0, 1000) > mutationThreshold):
        rndR1 = random.randrange(30, len(ch1))
        ch1 = setMutation(ch1, rndR1)

        rndR2 = random.randrange(30, len(ch2))
        ch2 = setMutation(ch2, rndR2)

        if (bin2float(ch1) >= a and bin2float(ch1) <= b):
            inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
            newGeneration.append(inhabitant)
        if (bin2float(ch2) >= a and bin2float(ch2) <= b):
            inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
            newGeneration.append(inhabitant)

print("Какой метод скрещивания использовать?: \n"
      "0 - Стандартный \n"
      "1 - Одноточечный \n"
      "2 - Одноточечный с возможностью перезаписи одного из родителей \n"
      "3 - Двуточечный \n"
      "4 - Равномерный \n")

crossoverMethod = input()

print("Какой метод отбора использовать?: \n"
      "0 - Ранговый \n"
      "1 - Пропорциональный \n"
      "2 - Турнирный \n"
      "3 - Турнирный с возвращением \n")

selectionMethod = input()

for r in range(0, 20):
    while(len(newGeneration) < len(inhabitants) * 2):
        pair = []
        while len(pair) < 2:
            #Случайным образом получаем особь
            rndNum = random.randrange(0, len(inhabitants))
            pair.append(inhabitants[rndNum])

        match crossoverMethod:
            case '0':
                StandartCrossover()
            case '1':
                OnePointCrossover()
            case '2':
                OnePointCrossoverWithCopy()
            case '3':
                TwoPointCrossover()
            case '4':
                EvenlyCrossover()
            case _:
                "Ошибка ввода на этапе выбора метода скрещивания"
                exit(-1)

    aliveNewGeneration = []
    SetWeight(newGeneration)

    match selectionMethod:
        case '0':
            Rank()
        case '1':
            Proportional()
        case '2':
            TournamentSelection()
        case '3':
            TournamentWithReturnSelection()
        case _:
            "Ошибка ввода на этапе выбора метода селекции"
            exit(-1)

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

