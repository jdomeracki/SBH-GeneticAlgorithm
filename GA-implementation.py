from math import *
from itertools import combinations
from operator import itemgetter
import random


def get_spectrum(file):
    spectrum = []
    with open(file, "r") as instance:
        for line in instance:
            spectrum.append(line.strip())
    return spectrum


def perfect_match(l_o_nct, r_o_nct):
    l = len(l_o_nct)
    r = len(r_o_nct)
    if (l == r):
        if (l_o_nct[1:] == r_o_nct[:r-1]):
            return l_o_nct + r_o_nct[-1:]
        elif (r_o_nct[1:] == l_o_nct[:l-1]):
            return r_o_nct + l_o_nct[-1:]
        else:
            return False
    elif (l > r):
        if (l_o_nct[1+l-r:] == r_o_nct[:r-1]):
            return l_o_nct + r_o_nct[-1:]
        elif (r_o_nct[1:] == l_o_nct[:r-1]):
            return r_o_nct + l_o_nct[-1+r-l:]
        else:
            return False
    elif (l < r):
        if (l_o_nct[1:] == r_o_nct[:l-1]):
            return l_o_nct + r_o_nct[-1+l-r:]
        elif (r_o_nct[1+r-l:] == l_o_nct[:l-1]):
            return r_o_nct + l_o_nct[-1:]
        else:
            return False


def find_match(spectrum):
    for i in range(len(spectrum)):
        for j in range(i+1, len(spectrum)):
            match = perfect_match(spectrum[i], spectrum[j])
            if(match):
                spectrum.pop(j)
                spectrum.pop(i)
                spectrum.insert(0, match)
                return spectrum
    return []


def get_avg(dct):
    x = 0
    for k in dct:
        x += len(dct[k])
    return ceil(x/len(dct))


def list_to_dict(lst):
    dct = {i: lst[i] for i in range(0, len(lst))}
    return dct


def optimize(spectrum):
    optimized = []
    while(True):
        current = find_match(spectrum)
        if(current):
            optimized = current
        else:
            break
    optimized = list_to_dict(optimized)
    return optimized


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


def merge(sequences):
    merged = sequences[0]
    for i in range(len(sequences)-1):
        l_seq = sequences[i]
        r_seq = sequences[i+1]
        overlap = get_overlap(l_seq, r_seq)
        merged += r_seq[overlap:]
    return merged


def get_num_of_ncts(optimized, keys, length):
    num_of_o_ncts = 0
    for key in keys:
        x = len(optimized[key])-length
        if (x == 0):
            num_of_o_ncts += 1
        else:
            num_of_o_ncts += 1+x
    return num_of_o_ncts


def generate_population(optimized, N, size_of_population):
    population = []
    n = len(optimized)
    k = int(ceil(n/2))
    for i in range(size_of_population):
        values = []
        keys = get_combination(n, k)
        for key in keys:
            values.append(optimized[key])
        population.append([keys, values])
    return population


def evaluate(population, optimized, initial_length, N):
    for seq in population:
        merged = merge(seq[1])
        seq.append(merged)
        merged_length = len(merged)
        num_of_o_ncts = get_num_of_ncts(optimized, seq[0], initial_length)
        fintess_score = (N-merged_length)+(num_of_o_ncts*2)
        seq.append(fintess_score)
    return population


def tournament(evaluated_population, size_of_population):
    contestants = get_combination(
        size_of_population, int(size_of_population*0.1))
    best_score = 0
    winner = None
    for contestant in contestants:
        fintess_score = evaluated_population[contestant][3]
        if (fintess_score > best_score):
            best_score = fintess_score
            winner = contestant
    return winner


def crossover():
    pass


def mutate():
    pass


def evolve():
    pass


if __name__ == "__main__":
    N = 209
    l = 10
    spectrum = get_spectrum("sample_instance.txt")
    # spectrum = ["AAT", "ACA", "ACG", "AGT",
    #            "CAA", "CAG", "CGA", "GTT", "TAC", "TCA"]
    optimized = optimize(spectrum)
    inital_population = generate_population(optimized, N, 100)
    evaluated_population = evaluate(inital_population, optimized, l, N)
    print(evaluated_population[tournament(evaluated_population, 100)])
    #sorted_by_fitness = sorted(evaluated_population, key=itemgetter(3))
    # for seq in sorted_by_fitness:
    #    print(seq)
    #    print("")
