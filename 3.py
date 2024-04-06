import math

def func (x, y):
    return math.sin(x) * math.cos(y)

def grad(x, y):
    return [math.cos(x) * math.cos(y), math.sin(x)*math.sin(y) * (-1)]

def norm(x, y):
    return math.sqrt((x + y) ** 2)

def newPoint(x, y, gradX, gradY, a, norma):
    x = x - a * (gradX / norma)
    y = y - a * (gradY / norma)
    return [x, y]

eps = 0.01
a = 0.01
values = [0.2, 0.7]
k = 0

y = func(values[0], values[1])
print("y", y)
gradient = grad(values[0], values[1])
print("gradient", gradient)
norma = eps + 1
print("norma", norma)
isSuccess = True
while(norma > eps and a > eps/1000000000.0):

    if(isSuccess):
        #pass
        gradient = grad(values[0], values[1])
        print("gradient", gradient)
        norma = norm(gradient[0], gradient[1])
        print("norma", norma)
        k = k + 1
        print("k", k)

    point = newPoint(values[0], values[1], gradient[0], gradient[1], a, norma)
    print("point", point)
    prevY = y
    print("prevY", prevY)
    newY = func(point[0], point[1])
    print("newY", newY)
    #print("___________________________________________________________________")

    if(newY < prevY):
        print("newY < prevY")
        isSuccess = True
        values[0] = point[0]
        values[1] = point[1]
        print("x, y", values[0], values[1])
        y = newY
        print("y", y)
        a = 1.25 * a
        print("a", a)
        print("___________________________________________________________________")
        if(k > 10000): break;
    else:
        print("newY > prevY")
        isSuccess = False
        a = 0.5 * a
        print("a", a)
        print("___________________________________________________________________")
        if (k > 10000): break;

print('X = ', values[0], 'Y = ', values[1], 'Value = ', y)





