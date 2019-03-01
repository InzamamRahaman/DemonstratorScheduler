import numpy as np
from deap import base
from deap import creator
from deap import tools
import random
import fitness

#https://groups.google.com/forum/#!topic/deap-users/FqOEGbLJsUQ


def init2d(icls, low, high, shape):
    indGenerator = np.random.randint(2,size=(32,64))
    return icls(indGenerator)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", init2d, creator.Individual,
low=0,high=2,shape=(32,64))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual,items):
    costs = []
    print("Inside")
    print(len(individual))
    for i in range(len(individual)):
        costs.append(fitness.fitness(individual[i],items[0],items[1],items[2],\
        items[3],items[4],items[5],0,0,0,0))
    return(costs)


#Genetic Operators
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

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
    pop = toolbox.population(n=10)
    print(type(pop[0]))
    seniority = np.random.randint(5,size=(D,L))
    time_per_lab = np.random.randint(5,size=(L,1))
    time_limits = np.random.randint(10,size=(D,1))
    demonstrator_requirements = np.random.randint(4,size=(L,1))
    items = [costs,qualifications,seniority,time_per_lab,time_limits\
    ,demonstrator_requirements]
    print(pop[0].fitness)

    
    print("after")
    #fitnesses = list(map(toolbox.evaluate,[pop,items]))
    fitnesses = toolbox.evaluate(pop,items)
    #fitnesses = list(map(fitnesses,pop))
    #fitnesses = (map(fitnesses, pop))
    #fitnesses = list(zip(fitnesses))
    print(fitnesses)
    print(max(fitnesses))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    #map(toolbox.evaluate,pop)

    offspring = toolbox.select(pop,len(pop))
    print("Offspring lenght: " + str(len(offspring)) )
    print(len(pop))

    i = 0

    for child1,child2 in zip(offspring[::2], offspring[1::2]):
        if(random.random() < CXPB):
            #print(child1)
            #print(child2)
            i+=1
    print("Number of children: ",i)
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

if __name__ == "__main__":
    main()
