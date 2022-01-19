import math

def f1(x):
    return sum(x)

def f2(x):
    ix_i = []
    for i in range(len(x)):
            ix_i.append(i*x[i])
    return sum(ix_i)

def f3(x):
    prod = []
    for i in range(len(x)):
        prod_ = 1
        for j in range(i+1):
            prod_ = x[j] * prod_
        prod.append(prod_)
    return  sum(prod)


def f4(x):
    sum_ = sum(x)
    if sum_ == 0 or sum_ == 6:
        return 1
    if sum_ == 1 or sum_ == 5:
        return 0
    if sum_ == 2 or sum_ == 4:
        return 0.360384
    if sum_ == 3:
        return 0.640576

def f5(x):
    sums = [sum(x[:3]), sum(x[3:])]
    u_x = []
    for i in sums:
        if i == 0:
            u_x.append(1)
        if i == 1:
            u_x.append(0)
        if i == 2 :
            u_x.append(0.360384)
        if i == 3:
            u_x.append(0.640576)
    return sum(u_x)


def f6(x):
    sum_ = sum(x)
    if sum_ <= 5:
        return 1 - 0.2*sum_
    else:
        return 6

def f7(x):
    sums = [sum(x[:3]), sum(x[3:])]
    u_x = []
    for i in sums:
        if i <= 2:
            u_x.append(1 - 0.2 * i)
        else:
            u_x.append(3)
    return sum(u_x)




