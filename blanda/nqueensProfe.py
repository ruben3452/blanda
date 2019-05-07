# coding: utf-8
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

NQUEENS = 8

def evalNQueens(individual):
    size = len(individual)
    ldiag = [0] * (2*size - 1)
    rdiag = [0] * (2*size - 1)

    for i in range(size):
        ldiag[i + individual[i]] += 1
        rdiag[size - 1 - i + individual[i]] += 1

    sum_ = 0
    for i in range(2*size - 1):
        if ldiag[i] > 1:
            sum_ += ldiag[i] - 1
        if rdiag[i] > 1:
            sum_ += rdiag[i] - 1
    return sum_

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness = creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(NQUEENS), NQUEENS)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalNQueens)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/NQUEENS)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(seed = 0):
    random.seed(seed)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    algorithms.eaSimple(pop,toolbox,cxpb=0.5,mutpb=0.2,ngen=100,stats=stats,halloffame=hof,verbose=True)

    return pop, stats, hof

if __name__ == '__main__':
    main()



