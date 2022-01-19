from deap import tools
import Utilities
from Utilities import S_RAND,S_LRS,S_QSO,S_RWS,S_SUS,S_TS
import random
import extra_selector_operators as exs
import QuantumWheel
import numpy
import math

from deap import base
from deap import creator
from deap import tools


def flip(c):
    return '1' if(c == '0') else '0';

def graytoInteger(gray):
    binary = "";

    # MSB of binary code is same
    # as gray code
    binary += gray[0];

    # Compute remaining bits
    for i in range(1, len(gray)):

        # If current bit is 0,
        # concatenate previous bit
        if (gray[i] == '0'):
            binary += binary[i - 1];

        # Else, concatenate invert
        # of previous bit
        else:
            binary += flip(binary[i - 1]);

    return int(binary, 2);

def x_var(lamba, x_low, x_up):
    return x_low + graytoInteger(lamba) * (x_up - x_low)/(math.pow(2,(len(lamba))) - 1 )


def off_ind(icls, ind_as_list):
    return icls(ind_as_list)

def create_offspring(toolbox,offspring_dict):
    offspring=[]
    toolbox.register('off_individual', off_ind, creator.Individual)
    for ind in list(offspring_dict.keys()):
        for iteration in range(offspring_dict[ind]):
            individuo = toolbox.off_individual(Utilities.string_to_list(ind))
            offspring.append(individuo)
    return offspring


def createToolbox(IND_SIZE, beta, provider_QGS):
    # Creating Classes
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register('attr_float', lambda: random.randint(0, 1))
    # individuo
    toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_float,
                 n=IND_SIZE)  # aggiunge individuo che è una lista di dim IND_SIZE
    # popolazione
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # operatori
    # Crossover
    toolbox.register('mate', tools.cxTwoPoint)
    # Mutation
    toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
    # Selection
    toolbox.register('select_TS', tools.selTournament)
    toolbox.register('select_RWS', tools.selRoulette)
    toolbox.register('select_RAND', tools.selRandom)
    toolbox.register('select_SUS', tools.selStochasticUniversalSampling)
    toolbox.register('select_LRS', exs.sel_LRS)
    toolbox.register('Q_select', QuantumWheel.QuantumWheel, n=IND_SIZE, beta=beta, provider=provider_QGS, backend_name='ibmq_qasm_simulator')
    toolbox.register("quality", Utilities.best_fitness, isMax=True)
    toolbox.register("diversity", Utilities.diversity2, IND_SIZE=IND_SIZE)
    return toolbox

def createStats():
    # Statistical Features
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    return stats




def updatedGA(toolbox, pop_size,  cxpb, mutpb, ngen,  selector, stats, pop_list=None,tourn_size=None, grv_iter=None, num_marked=3, hof = tools.HallOfFame(1), verbose=False):
    # Creating collector for Diversity and Quality Measurament
    Quality = []
    Diversity = []
    # Creating the population
    if pop_list==None:
        pop = toolbox.population(n=pop_size)
    else:
        pop = toolbox.clone(pop_list)

    # Defining the Logbook
    logbook = tools.Logbook()
    logbook.header = ["gen", "nevals"] + (stats.fields if stats else [])

    # Evaluate the entire population
    fitness = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitness):
        ind.fitness.values = [fit]

    hof.update(pop) if stats else {}

    record = stats.compile(pop) if stats else {}
    Quality.append(toolbox.quality(record))
    Diversity.append(toolbox.diversity(pop))
    logbook.record(gen=0, nevals=len(pop), **record)
    if verbose:
        print(logbook.stream)

    for g in range(ngen):

        # elitism
        bests = toolbox.clone(tools.selBest(pop, num_marked))
        elitist=bests[0]

        # Select the next generation individuals
        if selector == S_QSO:
            n2f = [Utilities.string_to_int(Utilities.list_to_string(bests[i])) for i in range(num_marked)]
            # print(n2f)
            # offspring_dict = toolbox.Q_select(n2f, shots=len(pop))
            offspring_dict = toolbox.Q_select(n2f=n2f, iterations=grv_iter, shots=pop_size)
            offspring = create_offspring(toolbox,offspring_dict)
        if selector == S_RWS:
            offspring = toolbox.select_RWS(pop, k=pop_size)
        if selector == S_TS:
            #print(POP_SIZE - len(off_2))
            offspring = toolbox.select_TS(pop, k=pop_size,  tournsize=tourn_size)
        if selector == S_RAND:
            offspring = toolbox.select_RAND(pop, k=pop_size)
        if selector == S_SUS:
            offspring = toolbox.select_SUS(pop, k=pop_size)
        if selector == S_LRS:
            offspring = toolbox.select_LRS(pop, k=pop_size)

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the entire population
        fitness = list(map(toolbox.evaluate, offspring))
        for ind, fit in zip(offspring, fitness):
            ind.fitness.values = [fit]

        # The population is entirely replaced by the offspring
        #pop = offspring
        pop[:] = tools.selBest(offspring, pop_size - 1)
        pop.append(elitist)

        hof.update(pop) if stats else {}

        record = stats.compile(pop) if stats else {}
        Quality.append(toolbox.quality(record))
        Diversity.append(toolbox.diversity(pop))
        # print(record)
        logbook.record(gen=g + 1, **record)
        if verbose:
            print(logbook.stream)

    return pop, logbook, Quality, Diversity