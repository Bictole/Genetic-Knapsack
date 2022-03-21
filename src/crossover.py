from random import randint


def single_point_crossover(a, b):
    if len(a) != len(b):
        raise ValueError("The two genomes needs to have the same length")

    length = len(a)
    if length < 2:
        return a, b
    
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]