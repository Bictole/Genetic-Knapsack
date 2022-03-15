from collections import namedtuple
from random import choices
import numpy as np

genome = []
population = []
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

def generate_genome(length: int):
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int):
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome, things, weight_limit):
    if len(genome) != len(things):
        raise ValueError("Genome and things length are not the same")
    
    weight = 0
    value = 0

    for i, things in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0
    
    return value