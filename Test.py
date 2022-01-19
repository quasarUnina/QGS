import genetic_algorithms as gs
from deap import tools
import random, json
import  Problems as Pb
import Utilities
import math, statistics, matplotlib.pyplot as plt
import os
from Utilities import S_RAND,S_LRS,S_QSO,S_RWS,S_SUS,S_TS
from genetic_algorithms import x_var


def test_selector(toolbox,selector, pop_size, cxpb, mutpb,mean_iter, n_gen, stats, n_marked_QGS = 3,  log_file=None, pop_list=None, grv_iter=None, tourn_size=None):
    Quality=[]
    Diversity=[]
    #output = open(log_file, "a")


    for iteration in range(mean_iter):
        print('iteration= ', iteration, ' selector= ', selector)
        #output.write('\n iteration= '+str(iteration)+' selector= '+str(selector)+'\n')
        if pop_list!=None:
            #print("yes")
            p_l=pop_list[iteration]
        if selector==S_QSO:
            #output.write('grover_iterations = '+ str(grv_iter) +'\n')
            GA_exe = gs.updatedGA(toolbox,pop_size,cxpb, mutpb, n_gen, selector=selector, stats=stats, pop_list=p_l, grv_iter=grv_iter, num_marked=n_marked_QGS, hof = tools.HallOfFame(1),verbose=False)
        else:
            GA_exe = gs.updatedGA(toolbox,pop_size,cxpb, mutpb, n_gen, selector=selector, stats=stats, pop_list=p_l, tourn_size=tourn_size, hof = tools.HallOfFame(1),verbose=False)
        #print(GA_exe)
        #output.write(json.dumps(GA_exe[1]))

        Quality.append(GA_exe[2])
        Diversity.append(GA_exe[3])
    #output.close()

    D = {}
    Q = {}
    for t in range(0,n_gen+1):
        Diversity_values = []
        Quality_values = []
        for k in range(mean_iter):
            Diversity_values.append(Diversity[k][t])
            Quality_values.append(Quality[k][t])
        D[t] = statistics.mean(Diversity_values)
        Q[t] = statistics.mean(Quality_values)
    return Q,D

'''
#HYPER-PARAMETERS
IND_SIZE = 5
beta = math.pi/4

mean_iter = 20
num_generations = 5
pop_size = 5
cxpb = 0.8
mutpb = 0.1

functions = [Pb.f_1, Pb.f_2, Pb.f_3, Pb.f_4, Pb.f_5, Pb.f_6]
boundaries = [[2.7,7.5], [0,4], [-5,5], [0,13], [0.001, 0.99], [3.1, 20.4]]
#grover_iters = [3,5,8]
grover_iters = [2,3,4]
tourn_size = [2,3,5]

toolbox=gs.createToolbox(IND_SIZE,beta)
stats=gs.createStats()
list_pop=[]
for k in range(mean_iter):
    list_pop.append(toolbox.population(n=pop_size))

for i in range(6):
    def evaluate(individual, x_low, x_up):
        x = x_var(Utilities.list_to_string(individual), x_low, x_up)
        return functions[i](x)

    toolbox.register('evaluate', evaluate, x_low=boundaries[i][0], x_up=boundaries[i][1])
    print('f_'+str(i+1))
    log_path = './plots/'+str(IND_SIZE)+'q/jakarta/f_'+str(i+1)+'/'
    log_name = 'log_stats_tuned.txt'
    fig_path = './plots/'+str(IND_SIZE)+'q/jakarta/f_'+str(i+1)+'/'
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    if not os.path.isdir(fig_path):
        os.makedirs(fig_path)

    selectors=[S_RWS, S_SUS, S_TS, S_LRS, S_RAND, S_QSO]
    colors={S_RWS:"orange",S_SUS: "magenta", S_TS:"purple", S_LRS:"red", S_RAND: "green", S_QSO:"blue"}


    dict={}
    for sel in selectors:
        dict[sel]=test_selector(toolbox,selector=sel, tourn_size=2,  grv_iter=grover_iters[0],pop_size=pop_size,cxpb=cxpb, mutpb=mutpb, mean_iter=mean_iter, n_gen=num_generations, log_file=log_path+log_name, stats=stats, pop_list = list_pop)
        Utilities.writeListToFile(log_path + 'Average_fitness_' + 'f_' + str(i + 1) + "_"+sel+'.txt', list(dict[sel][0].values()))
        Utilities.writeListToFile(log_path + 'Diversity_' + 'f_' + str(i + 1) + "_"+sel+ '.txt',
                                  list(dict[sel][1].values()))

    fig_c = plt.figure(1)

    for sel in selectors:
        plt.plot(list(dict[sel][0].keys()), list(dict[sel][0].values()), color=colors[sel], label=sel)

    plt.title(r'Average fitness ' + '$f_' + str(i+1)+'$')
    plt.xlabel('generation')
    plt.legend()
    #plt.yscale('log')
    plt.savefig(fig_path+'Average_fitness_' + 'f_' + str(i+1)+ '.png')
    plt.close(fig_c)
    plt.show()

    fig_q = plt.figure(2)

    for sel in selectors:
        plt.plot(list(dict[sel][1].keys()), list(dict[sel][1].values()), color=colors[sel], label=sel)

    plt.title(r'Diversity ' + '$f_' + str(i+1)+'$')
    plt.xlabel('generation')
    plt.legend()
    plt.savefig(fig_path+'Diversity_'+ 'f_' + str(i+1) + '.png')
    plt.close(fig_q)
    plt.show()
    
'''    
'''

    cols=['orange','red','green']
    dict_qso = {}
    for grv_iter in grover_iters:
        dict_qso[grv_iter] = test_selector(toolbox, selector=S_QSO, grv_iter=grv_iter, pop_size=pop_size,
                                           cxpb=cxpb, mutpb=mutpb, mean_iter=mean_iter, n_gen=num_generations,
                                           log_file=log_path + log_name, stats=stats, pop_list=list_pop)
        Utilities.writeListToFile(log_path + 'Average_fitness_' + 'f_' + str(i + 1) + "_"+str(grv_iter)+'.txt', list(dict_qso[grv_iter][0].values()))
        Utilities.writeListToFile(log_path + 'Diversity_' + 'f_' + str(i + 1) + "_"+str(grv_iter)+ '.txt',
                                  list(dict_qso[grv_iter][1].values()))

    fig_c = plt.figure(1)

    h=0
    for grv_iter in grover_iters:
        plt.plot(list(dict_qso[grv_iter][0].keys()), list(dict_qso[grv_iter][0].values()), color=cols[h], label="QSO_"+str(grv_iter))
        h+=1

    plt.title(r'Average fitness ' + '$f_' + str(i + 1) + '$')
    plt.xlabel('generation')
    plt.legend()
    # plt.yscale('log')
    plt.savefig(fig_path + 'Average_fitness_' + 'f_' + str(i + 1) + '.png')
    plt.close(fig_c)
    plt.show()

    fig_q = plt.figure(2)

    h=0
    for grv_iter in grover_iters:
        plt.plot(list(dict_qso[grv_iter][1].keys()), list(dict_qso[grv_iter][1].values()),
                 color=cols[h], label="QSO_" + str(grv_iter))
        h+=1

    plt.title(r'Diversity ' + '$f_' + str(i + 1) + '$')
    plt.xlabel('generation')
    plt.legend()
    plt.savefig(fig_path + 'Diversity_' + 'f_' + str(i + 1) + '.png')
    plt.close(fig_q)
    plt.show()


    dict_ts = {}
    for t in tourn_size:
        dict_ts[t] = test_selector(toolbox, selector=S_TS, tourn_size=t, pop_size=pop_size,
                                   cxpb=cxpb, mutpb=mutpb, mean_iter=mean_iter, n_gen=num_generations,
                                   log_file=log_path + log_name, stats=stats, pop_list=list_pop)

    fig_c = plt.figure(1)

    for t in tourn_size:
        plt.plot(list(dict_ts[t][0].keys()), list(dict_ts[t][0].values()),
                 color=list(colors.values())[t], label="TS_" + str(t))

    plt.title(r'Average fitness ' + '$f_' + str(i + 1) + '$')
    plt.xlabel('generation')
    plt.legend()
    # plt.yscale('log')
    plt.savefig(fig_path + 'Average_fitness_' + 'f_' + str(i + 1) + '.png')
    plt.close(fig_c)
    plt.show()

    fig_q = plt.figure(2)

    for t in tourn_size:
        plt.plot(list(dict_ts[t][1].keys()), list(dict_ts[t][1].values()),
                 color=list(colors.values())[t], label="TS_" + str(t))

    plt.title(r'Diversity ' + '$f_' + str(i + 1) + '$')
    plt.xlabel('generation')
    plt.legend()
    plt.savefig(fig_path + 'Diversity_' + 'f_' + str(i + 1) + '.png')
    plt.close(fig_q)
    plt.show()
'''







