import numpy as np
from deap import base
from deap import creator
from deap import tools
import fitness

#https://groups.google.com/forum/#!topic/deap-users/FqOEGbLJsUQ


def init2d(icls, low, high, shape):
    indGenerator = np.random.randint(2,size=(32,64))
    return indGenerator


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", init2d, creator.individual,
low=0,high=2,shape=(32,64))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)


def evalOneMax(individual):
    print("Here")
    li = []
    for i in individual:
        sum = 0
        for j in i:
            if(j == 1):
                sum+=1
        li.append(sum)

        #print(i,"\n")
    #print(individual,"\n")
    return li


#Genetic Operators
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

#pop = toolbox.population(n=1)



def main():
    L = 64
    D = 32
    costs = np.random.randint(-20,20,size=(L,L))
    qualifications = np.random.randint(2,size=(D,L) )
    pop = toolbox.population(n=2)
    seniority = np.random.randint(5,size=(D,L))
    time_per_lab = np.random.randint(5,size=(L,1))
    time_limits = np.random.randint(10,size=(D,1))
    demonstrator_requirements = np.random.randint(4,size=(L,1))
    #print(pop[0])
    #print(len(pop))
    value = fitness.fitness(pop[0],costs,qualifications,seniority,time_per_lab\
    ,time_limits,demonstrator_requirements,0,0,0,0)
    print(value)
    '''
    print(pop)
    print(len(pop))
    print(len(pop[0]))
    print(type(pop))
    print(np.shape(pop))
    print(pop[0][0])
    '''
    fitnesses = list(map(toolbox.evaluate, pop))

    #Evaluation the entire population
    '''
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    CXPB, MUTPB = 0.5, 0.2

    fits = [ind.fitness.values for ind in pop]
    print(max(fitnesses))
    print(fitnesses)
    print(fits)
    #print(len(fitnesses))
    #print(len(fitnesses[0]))
    '''

if __name__ == "__main__":
    main()
