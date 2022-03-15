from collections import namedtuple
from random import choices
from typing import Callable
import numpy as np

Genome = []
population = []
FitnessFunc = Callable[[Genome], int]
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192)
]

more_things = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70)
]

def generate_genome(length: int):
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int):
    return [generate_genome(genome_length) for _ in range(size)]

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

