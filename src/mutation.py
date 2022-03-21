from random import randrange, random


def mutation(genome, num = 1, probability = 0.5):
    for _ in range(len(genome)):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    
    return genome