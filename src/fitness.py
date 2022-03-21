from random import choices
from typing import Callable, List

Genome = List[int]
FitnessFunc = Callable[[Genome], int]


def fitness(genome, things, weight_limit):
    if len(genome) != len(things):
        raise ValueError("Genome and things length are not the same")
    
    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0
    
    return value

def selection_pair(population, fitness_func):
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )