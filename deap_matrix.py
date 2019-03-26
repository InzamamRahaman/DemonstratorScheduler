'''
Call function instead when using the fitness.py update code to suit

'''

import numpy as np
from deap import base
from deap import creator
from deap import tools
import random
import fitness
from matplotlib import pyplot as plt

#https://groups.google.com/forum/#!topic/deap-users/FqOEGbLJsUQ
#Elitism https://groups.google.com/forum/#!topic/deap-users/iannnLI2ncE


def init2d(icls, low, high, shape):
    indGenerator = np.random.randint(2,size=(32,64))
    return icls(indGenerator)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", init2d, creator.Individual,
low=0,high=2,shape=(32,64))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual,items):
    costs = []
    print("Inside")
    #print(len(individual))
    for i in range(len(individual)):
        costs.append( tuple([fitness.fitness(individual[i],items[0],items[1],items[2],\
        items[3],items[4],items[5],0,0,0,0)]) )
    return(costs)

def mutate(individual):
    row = random.randint(0,individual.shape[0]-1)
    col = random.randint(0,individual.shape[1]-1)
    #print(individual[row][col])
    individual[row][col] = 1 - (individual[row][col]) 
    #print("Here ", individual[row][col])
    #return row,col



#Genetic Operators
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate)

'''Not sure if I'm doing this correctly
in the example it seemed like they just copied the 
lists, like a copy of the population because you will be updating 
the offspring'''
#toolbox.register("select", np.copy)
toolbox.register("select", tools.selTournament, tournsize=3)

#pop = toolbox.population(n=1)



def main():
    '''Might need to change the random function, will need to discuss this'''
    random.seed(64)
    L = 64
    D = 32
    CXPB, MUTPB = 0.5, 0.2

    costs = np.random.randint(-20,20,size=(L,L))
    qualifications = np.random.randint(2,size=(D,L) )
    pop = toolbox.population(n=20)
    #print(type(pop[0]))
    seniority = np.random.randint(5,size=(D,L))
    time_per_lab = np.random.randint(5,size=(L,1))
    time_limits = np.random.randint(10,size=(D,1))
    demonstrator_requirements = np.random.randint(4,size=(L,1))
    items = [costs,qualifications,seniority,time_per_lab,time_limits\
    ,demonstrator_requirements]
    print(pop[0].fitness)

    
    print("after")
    #fitnesses = list(map(toolbox.evaluate,[pop,items]))
    fitnesses = toolbox.evaluate(pop,items=items)
    #fitnesses = list(map(fitnesses,pop))
    #fitnesses = (map(fitnesses, pop))
    #fitnesses = list(zip(fitnesses))
    #print(list(fitnesses))
    print((fitnesses))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    #map(toolbox.evaluate,pop)

    fits = [ind.fitness.values[0] for ind in pop]

    #print(fits)
    #print(pop[0].fitness)

    g = 0
    minimum = []

    while(max(fits) < 100 and g < 5):
        elite = tools.selBest(pop, int(0.1*len(pop)))
        print("Elites ",len(elite))
        print([x.fitness.values for x in elite])
        pop = pop[2:]
        print("Population",len(pop))
        print([x.fitness.values for x in pop])
        g+=1
        print("\n\n-- Generation %i -- \n\n" %g)

        offspring = toolbox.select(pop,len(pop))
        offspring = list(map(toolbox.clone,offspring))

        i = 0

        for child1,child2 in zip(offspring[::2], offspring[1::2]):
            if(random.random() < CXPB):
                #print(child1)
                #print(child2)
                i+=1
                #print("It's here")
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                '''
                print(type(mutant))
                print(mutant)
                print(mutant[0][0])
                '''
                '''
                if(mutant[0][0]):
                    mutant[0][0] = 0
                else:
                    mutant[0][0] = 1
                '''
                #print(mutant[0][0])
                #print(mutant.shape)
                #print(mutant.shape[0])
                #row,col = toolbox.mutate(mutant)
                toolbox.mutate(mutant)
                #print(mutant[row][col])
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.evaluate(invalid_ind,items=items)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        elite += pop
        pop = elite
        fits = [ind.fitness.values[0] for ind in pop]
        print("Length with elites back: ",len(pop))
        

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2/length - mean**2)**0.5
        print(fits)

        min1 = min(fits)
        minimum+=[min1]
        #print(minimum)
        print("  Min %s" % min1)
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        #Evaluation the entire population
        '''
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit


        fits = [ind.fitness.values for ind in pop]
        print(max(fitnesses))
        print(fitnesses)
        print(fits)
        #print(len(fitnesses))
        #print(len(fitnesses[0]))
        '''
    
    print("\n\nTotal minimum values\n\n",minimum)
    plt.plot(minimum,marker='x')
    plt.savefig('ga.png')
    plt.show()

if __name__ == "__main__":
    main()
