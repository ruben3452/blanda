# coding: utf-8
import random

NQUEENS = 8
NPoblacion
GENMAX

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
