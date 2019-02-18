import numpy as np
from deap import base
from deap import creator
from deap import tools

#https://groups.google.com/forum/#!topic/deap-users/FqOEGbLJsUQ


def init2d(icls, low, high, shape):
    indGenerator = np.random.randint(low,high,shape)
    return icls(indGenerator)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", init2d, creator.individual,
low=0,high=2,shape=(32,64))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

pop = toolbox.population(n=2)
print(len(pop))
print(len(pop[0]))
print(type(pop))
print(np.shape(pop))