from collections import namedtuple
from functools import partial
from multiprocessing.sharedctypes import Value
from random import choices, randint, randrange, random
from typing import Callable, List, Tuple
from unittest import result
from xml.dom import ValidationErr
import numpy as np
import time

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

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
] + things

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

def single_point_crossover(a, b):
    if len(a) != len(b):
        raise ValueError("The two genomes needs to have the same length")

    length = len(a)
    if length < 2:
        return a, b
    
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome, num = 1, probability = 0.5):
    for _ in range(len(genome)):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    
    return genome

def run_evolution(
    populate_func,
    fitness_func,
    fitness_limit,
    selection_func = selection_pair,
    crossover_func = single_point_crossover,
    mutation_func = mutation,
    generation_limit = 100):
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population)/ 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, i


start = time.time()

population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length = len(more_things)
    ),
    fitness_func=partial(
        fitness, things=more_things, weight_limit=3000
    ),
    fitness_limit=1310,
    generation_limit=100
)

end = time.time()

def genome_to_things(genome, _things):
    result = []
    for i, thing in enumerate(_things):
        if genome[i] == 1:
            result += [thing.name]
    
    return result

print(f"number of generations: {generations}")
print(f"time: {end - start}s")
print(f"best solution {genome_to_things(population[0], more_things)}")

