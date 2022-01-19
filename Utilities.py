import numpy
import json

S_RWS="RWS"
S_TS="TS"
S_SUS="SUS"
S_LRS="LRS"
S_RAND="Random"
S_QSO="QGS"


def string_to_list(string):
    """Function that transform a string such as '01110'
    in a list such as [0,1,1,1,0]"""
    l = list(string)
    return [int(i) for i in l]

def list_to_string(l):
    """Function that transform a a list such as [0,1,1,1,0]
    in string such as '01110' """
    s=''
    for i in l:
        s = s + str(i)
    return s


def string_to_int(s):
    return int(s,2)


def new_pop(dictionary):
    '''Function that transforms the QuantumWheel output in the new pop
    _____________________________________________________________________
    Input: {ind: How many times the ind must be included in the population}
    Output: population as list.
    ______________________________________________________________________
    '''
    pop = []
    for ind in list(dictionary.keys()):
        for iteration in range(dictionary[ind]):
            pop.append(string_to_list(ind))
    return pop

def product(x):
    prod = 1
    for i in x:
        prod = prod * i
    return prod


def hamming_distance(chr1, chr2):
    count=0
    for i in range(len(chr1)):
        if chr1[i]!=chr2[i]:
            count+=1
    return count

def diversity2(pop, IND_SIZE):
    d_ij_list = []
    for i in range(len(pop)):
        for j in range(len(pop)):
            if i == j:
                continue
            else:
                d_ij_list.append(hamming_distance(numpy.array(pop[i]),numpy.array(pop[j])))
                # print('max', max(d_ij_list))
    #return (sum(d_ij_list)/2) / (len(pop)**2*IND_SIZE/2)
    return (sum(d_ij_list)) / (len(pop)*(len(pop)-1)*(IND_SIZE-1))

def best_fitness(record, isMax):
    if isMax:
        return record['max']
    else:
        return record['min']

def writeListToFile(filename, basicList):
    with open(filename, 'w') as filehandle:
        json.dump(basicList, filehandle)

def readListFromFile(filename):
    with open(filename, 'r') as filehandle:
        basicList = json.load(filehandle)
    return basicList

