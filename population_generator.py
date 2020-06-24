# Standard and third party libraries
from math import *
from itertools import combinations, permutations
import random


def get_combination(n, k):
    return random.sample(range(0, n), k)


def get_overlap(l_seq, r_seq):
    overlap = 0
    x = min(len(l_seq), len(r_seq))
    for i in range(1, x):
        if(l_seq[-i:] == r_seq[:i]):
            overlap += 1
        else:
            break
    return overlap


def get_avg(dct):
    x = 0
    for k in dct:
        x += len(dct[k])
    return ceil(x/len(dct))


def merge(sequences):
    merged = sequences[0]
    overlap_count = 0
    for i in range(len(sequences)-1):
        l_seq = sequences[i]
        r_seq = sequences[i+1]
        overlap = get_overlap(l_seq, r_seq)
        merged += r_seq[overlap:]
        overlap_count += overlap
    return merged, overlap_count


def get_num_of_ncts(optimized, keys, length):
    num_of_o_ncts = 0
    for key in keys:
        x = len(optimized[key])-length
        if (x == 0):
            num_of_o_ncts += 1
        else:
            num_of_o_ncts += 1+x
    return num_of_o_ncts


def generate_population(optimized, size_of_population, key_of_best, N):
    population = []
    n = len(optimized)
    avg = int(ceil(N/get_avg(optimized)))
    for i in range(size_of_population):
        values = []
        k = random.randint(1, avg)
        keys = get_combination(n, k)
        toss = random.uniform(0, 1)
        if(toss <= 0.1 and key_of_best not in keys):
            keys.insert(0, key_of_best)
        for key in keys:
            values.append(optimized[key])
        population.append([keys, values])
    return population


def evaluate(population, optimized, initial_length, N):
    for seq in population:
        merged, overlaps = merge(seq[1])
        seq.append(merged)
        merged_length = len(merged)
        seq.append(merged_length)
        num_of_o_ncts = get_num_of_ncts(optimized, seq[0], initial_length)
        fitness_score = overlaps + num_of_o_ncts - abs(N-merged_length)
        seq.append(fitness_score)
        seq.append(num_of_o_ncts)
    return population
