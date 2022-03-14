from random import choices
import numpy as np

genome = []
population = []

def generate_genome(length: int):
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int):
    return [generate_genome(genome_length) for _ in range(size)]