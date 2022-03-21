from collections import namedtuple
from functools import partial
from typing import Callable, List, Tuple
import time

from src import generation, fitness, crossover, mutation

Genome = List[int]
FitnessFunc = Callable[[Genome], int]
Population = List[Genome]
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

def run_evolution(
    populate_func,
    fitness_func,
    fitness_limit,
    selection_func = fitness.selection_pair,
    crossover_func = crossover.single_point_crossover,
    mutation_func = mutation.mutation,
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

def genome_to_things(genome, _things):
    result = []
    for i, thing in enumerate(_things):
        if genome[i] == 1:
            result += [thing.name]
    
    return result

if __name__ == "__main__":
    start = time.time()

    population, generations = run_evolution(
        populate_func=partial(
            generation.generate_population, size=10, genome_length = len(more_things)
        ),
        fitness_func=partial(
            fitness.fitness, things=more_things, weight_limit=3000
        ),
        fitness_limit=1310,
        generation_limit=100
    )

    end = time.time()

    print(f"number of generations: {generations}")
    print(f"time: {end - start}s")
    print(f"best solution {genome_to_things(population[0], more_things)}")