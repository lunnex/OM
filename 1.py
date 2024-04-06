a = -1
b = 1
x = 0
eps = 0.001


#max
def func (x):
    return x*x+1

def dih(a, b, eps):
    while(abs(a - b) > 2 * eps):
        x = (a + b) / 2
        gamma1 = x - eps / 2
        gamma2 = x + eps / 2
        y1 = func(gamma1)
        y2 = func(gamma2)
        if(y1 < y2):
            a = gamma1
        else:
            b = gamma2
    print("gamma opt")
    print(round((a + b) / 2, 3))

    print("f opt")
    print(round(func((a + b) / 2), 3))

import numpy as np

def getN(a, b, eps):
    fibArray = np.array([0, 1, 1])
    l = abs(a - b) / eps

    i = 2
    while (fibArray[i] < l):
        num = fibArray[i] + fibArray[i - 1]
        fibArray = np.append(fibArray, num)
        i = i + 1
    return i, fibArray

def fib(a, b, eps):
    (n, fibArray) = getN(a, b, eps)
    gamma1 = a + fibArray[n - 1] / fibArray[n] * (abs(b - a))
    gamma2 = b - fibArray[n - 1] / fibArray[n] * (abs(b - a))

    f1 = func(gamma1)
    f2 = func(gamma2)

    lastGamma = 0

    while(n > 2):
        if(f1 < f2):
            b = gamma1
            f1 = f2
            gamma1 = gamma2
            gamma2 = b - fibArray[n - 2] / fibArray[n - 1] * (b - a)
            f2 = func(gamma2)
            lastGamma = gamma2
        else:
            a = gamma1
            f2 = f1
            gamma2 = gamma1
            gamma1 = a + fibArray[n - 2] / fibArray[n - 1] * (b - a)
            f1 = func(gamma1)
            lastGamma = gamma1
        n = n - 1

    if(f1 < f2):
        print("gamma opt")
        print(round(lastGamma, 3))

        print("f opt")
        print(round(f1, 3))
    else:
        print("gamma opt")
        print(round(lastGamma, 3))

        print("f opt")
        print(round(f2, 3))

def gs(a, b, eps):
    t = 0.618
    counter = 0

    while(abs(a - b) / 2 > eps):
        counter += 1
        l = abs(b-a)
        gamma1 = a + l * t
        gamma2 = b - l * t

        y1 = func(gamma1)
        y2 = func(gamma2)

        print('l', l)
        #print('gamma2', gamma2)
        print('gamma1', gamma1)
        print('gamma2', gamma2)
        print('y1', y1)
        print('y2', y2)
        print('a', a)
        print('b', b)

        if (y1 > y2):
            b = gamma1
            y1 = y2
            gamma1 = gamma2
            gamma2 = a + (b - gamma1)
            print('gamma1', gamma1)
            print('gamma2', gamma2)
            y2 = func(gamma2)
            print('y1', y1)
            print("_____________________")
        else:
            a = gamma2
            y2 = y1
            gamma2 = gamma1
            gamma1 = b - (gamma2 - a)
            print('gamma1', gamma1)
            print('gamma2', gamma2)
            y1 = func(gamma1)
            print('y1', y1)
            print("_____________________")

    if (y1 < y2):
        print("gamma opt")
        print(round(gamma1, 3))

        print("f opt")
        print(round(y1, 3))
    else:
        print("gamma opt")
        print(round(gamma2, 3))

        print("f opt")
        print(round(y2, 3))


dih(a, b, eps)
fib(a, b, eps)
gs(a, b, eps)
