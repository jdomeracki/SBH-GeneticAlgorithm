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
    # random.shuffle(spectrum)
    for i in range(len(spectrum)):
        for j in range(i+1, len(spectrum)):
            match = perfect_match(spectrum[i], spectrum[j])
            if(match):
                spectrum.pop(j)
                spectrum.pop(i)
                spectrum.insert(0, match)
                # spectrum.append(match)
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


def generate_population(optimized, size_of_population, N):
    population = []
    n = len(optimized)
    k = int(ceil(N/get_avg(optimized)))
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
        seq.append(merged_length)
        num_of_o_ncts = get_num_of_ncts(optimized, seq[0], initial_length)
        fitness_score = num_of_o_ncts
        seq.append(fitness_score)
    return population


def find_best_seq(list_of_seqs, N):
    best_score = 0
    best_seq = None
    for seq in list_of_seqs:
        fintess_score = seq[4]
        seq_length = seq[3]
        if (fintess_score > best_score and seq_length <= N):
            best_score = fintess_score
            best_seq = seq
    return best_seq


def find_worst_seq(list_of_seqs, N):
    worst_score = 10000
    worst_seq_id = None
    for seq in list_of_seqs:
        fintess_score = seq[1][4]
        if (fintess_score < worst_score):
            worst_score = fintess_score
            worst_seq_id = seq[0]
    return worst_seq_id


def get_best_seq(evaluated_population, N):
    best_seq = find_best_seq(evaluated_population, N)
    return best_seq


def tournament(evaluated_population, size_of_population, N):
    contestants = []
    lottery_picks = get_combination(
        size_of_population, int(size_of_population*0.1))
    for pick in lottery_picks:
        contestants.append(evaluated_population[pick])
    winner_id = find_best_seq(contestants, N)
    return winner_id


def remove_duplicates(children, list_of_keys):
    for child in children:
        keys = []
        duplicates = []
        for i in range(len(child[0])):
            if(child[0][i] in keys):
                duplicates.append(i)
            else:
                keys.append(child[0][i])
        for duplicate in duplicates:
            while(True):
                replace_with = random.choice(list_of_keys)
                if(replace_with not in keys):
                    child[0][duplicate] = replace_with
                    keys.append(replace_with)
                    break
    return children


def map_from_optimized(children, optimized):
    for child in children:
        o_ncts = []
        for i in range(len(child[0])):
            o_ncts.append(optimized[child[0][i]])
        child.append(o_ncts)
    return children


def mutate(children, optimized):
    for child in children:
        list_of_keys = child[0]
        key_id = random.randint(0, len(child[0])-1)
        while(True):
            replace_with = random.randint(0, len(optimized)-1)
            if(replace_with not in list_of_keys):
                child[0][key_id] = replace_with
                break
    return children


def verify_if_fit_and_legal(children, l_parent, r_parent, N):
    fit_legal_children = []
    for child in children:
        child_score = child[4]
        child_length = child[3]
        l_parent_score = l_parent[4]
        r_parent_score = r_parent[4]
        if (((child_score > l_parent_score) or (child_score > r_parent_score)) and (child_length <= N)):
            fit_legal_children.append(child)
    return fit_legal_children


def crossover(l_parent, r_parent, optimized, l, N):
    l_cuts, r_cuts, children = [], [], []
    list_of_keys = l_parent[0] + r_parent[0]
    l_seq_num = len(l_parent[0])
    r_seq_num = len(r_parent[0])
    mulps = [0.25, 0.5, 0.75]
    for mulp in mulps:
        l_cuts.append(int(ceil(l_seq_num*mulp)))
        r_cuts.append(int(ceil(r_seq_num*mulp)))
    l_cuts.append(l_seq_num)
    r_cuts.append(r_seq_num)
    children.append([l_parent[0][:l_cuts[0]] + r_parent[0][r_cuts[0]:r_cuts[1]] +
                     l_parent[0][l_cuts[1]:l_cuts[2]] + r_parent[0][r_cuts[2]:]])
    children.append([r_parent[0][:r_cuts[0]] + l_parent[0][l_cuts[0]:l_cuts[1]] +
                     r_parent[0][r_cuts[1]:r_cuts[2]] + l_parent[0][l_cuts[2]:]])
    children.append([l_parent[0][:l_cuts[0]] + l_parent[0][l_cuts[0]:l_cuts[1]] +
                     r_parent[0][r_cuts[1]:r_cuts[2]] + r_parent[0][r_cuts[2]:]])
    children.append([r_parent[0][:r_cuts[0]] + r_parent[0][r_cuts[0]:r_cuts[1]] +
                     l_parent[0][l_cuts[1]:l_cuts[2]] + l_parent[0][l_cuts[2]:]])

    children = remove_duplicates(children, list_of_keys)
    children = mutate(children, optimized)
    children = map_from_optimized(children, optimized)
    children = evaluate(children, optimized, l, N)
    children = verify_if_fit_and_legal(children, l_parent, r_parent, N)

    return children


def survival_of_the_fittest(evaluated_population, size_of_population, N):
    contestants = []
    lottery_picks = get_combination(
        size_of_population, int(size_of_population*0.1))
    for pick in lottery_picks:
        contestants.append([pick, evaluated_population[pick]])
    loser_id = find_worst_seq(contestants, N)
    return loser_id


def evolve(population, size_of_population, optimized, N):
    for i in range(100):
        pop_children = []
        for i in range(50):
            l_parent = tournament(population, size_of_population, N)
            r_parent = tournament(population, size_of_population, N)
            children = crossover(
                l_parent, r_parent, optimized, l, N)
            for child in children:
                mutate
                pop_children.append(child)
        for child in pop_children:
            loser_id = survival_of_the_fittest(
                population, size_of_population, N)
            population[loser_id] = child
        #print(get_best_seq(population, N))


if __name__ == "__main__":
    N = 209
    l = 10
    size_of_population = int(N/2)
    spectrum = get_spectrum("sample_instance.txt")
    # spectrum = ["AAT", "ACA", "ACG", "AGT",
    #            "CAA", "CAG", "CGA", "GTT", "TAC", "TCA"]
    optimized = optimize(spectrum)
    inital_population = generate_population(optimized, size_of_population, N)
    evaluated_population = evaluate(inital_population, optimized, l, N)
    for seq in evaluated_population:
        print("Length: " + str(seq[3]) + " Score: " + str(seq[4]))
    print("")
    print("")
    print("")
    evolve(evaluated_population, size_of_population, optimized, N)
    for seq in evaluated_population:
        print("Length: " + str(seq[3]) + " Score: " + str(seq[4]))
    print("")
    print("")
    print("")
