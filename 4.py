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
        #print(float2bin(arr[i].x))
        #print(inhabitants[i].x, inhabitants[i].y, inhabitants[i].chance)
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

sizeOfGeneration = 10

inhabitants = []

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

#printGeneration()
#print("_________________________________________________________________________________")

#Создание нового поколения
newGeneration = []


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

        for i in distribution:
            if(x > i[0] and x < i[1]):
                aliveNewGeneration.append(distribution[i])


def Rank():
    pass

    #print(distribution)


for r in range(0, 20):
    while(len(newGeneration) < len(inhabitants) * 2):
        pair = []
        while len(pair) < 2:
            #Случайным образом получаем особь
            rndNum = random.randrange(0, len(inhabitants))
            pair.append(inhabitants[rndNum])

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

        #Мутация
        if(random.randrange(0, 1000) > 950):
            ch1 = s1 + p11 + p22 + m11 + m22
            rndR1 = random.randrange(30, len(ch1))
            ch1 = setMutation(ch1, rndR1)

            floatCh1 = bin2float(ch1)
            #print(floatCh1)

            ch2 = s2 + p12 + p21 + m12 + m21
            rndR2 = random.randrange(30, len(ch2))
            ch2 = setMutation(ch2, rndR2)

            floatCh2 = bin2float(ch2)
            #print(floatCh2)

            if(bin2float(ch1) >= a and bin2float(ch1) <= b):
                inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
                newGeneration.append(inhabitant)
            if(bin2float(ch2) >= a and bin2float(ch2) <= b):
                inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
                newGeneration.append(inhabitant)
        else:
            # Не мутация
            ch1 = s1 + p11 + p22 + m11 + m22
            ch2 = s2 + p12 + p21 + m12 + m21

            floatCh2 = bin2float(ch2)
            #print(floatCh2)
            floatCh1 = bin2float(ch1)
            #print(floatCh1)

            if (bin2float(ch1) >= a and bin2float(ch1) <= b):
                inhabitant = Inhabitant(bin2float(ch1), func(bin2float(ch1)))
                newGeneration.append(inhabitant)
            if (bin2float(ch2) >= a and bin2float(ch2) <= b):
                inhabitant = Inhabitant(bin2float(ch2), func(bin2float(ch2)))
                newGeneration.append(inhabitant)

    #Турнирный отбор
    aliveNewGeneration = []
    SetWeight(newGeneration)

    Proportional()

    # Дорогу молодым
    try:
        for i in range(0, len(inhabitants)):
            inhabitants[i] = aliveNewGeneration[i]
    except:
        print(len(aliveNewGeneration))

    #print('a')
    newGeneration = []

    #Расчет функции полезности для нового поколения
    SetWeight(inhabitants)

    printGeneration(aliveNewGeneration)


# турнирный отбор особи
