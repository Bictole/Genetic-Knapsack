from random import choices


def generate_genome(length):
    return choices([0, 1], k=length)

def generate_population(size, genome_length):
    return [generate_genome(genome_length) for _ in range(size)]