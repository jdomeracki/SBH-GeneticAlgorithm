# Standard and third party libraries
from math import *
from itertools import combinations
import random

# Local modules
from population_generator import evaluate, get_combination


def find_best_seq(list_of_seqs, N):
    best_score = -10000
    best_seq = None
    for seq in list_of_seqs:
        fintess_score = seq[4]
        seq_length = seq[3]
        if (fintess_score > best_score):  # and seq_length <= N):
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


def get_best_seq(list_of_seqs, N):
    best_score = -10000
    best_seq = None
    for seq in list_of_seqs:
        fintess_score = seq[4]
        seq_length = seq[3]
        if (fintess_score > best_score and seq_length <= N):
            best_score = fintess_score
            best_seq = seq
    return best_seq


def tournament(evaluated_population, size_of_population, N):
    contestants = []
    winner_id = None
    while(winner_id == None):
        lottery_picks = get_combination(
            size_of_population, int(size_of_population*0.05))
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


def mutate_by_insertion(child, optimized):
    list_of_keys = child[0]
    key_id = random.randint(0, len(child[0])-1)
    while(True):
        replace_with = random.randint(0, len(optimized)-1)
        if(replace_with not in list_of_keys):
            child[0][key_id] = replace_with
            break
    return child


def mutate_by_swap(child):
    size_of_child = len(child[0])
    child_seq = child[0]
    index_a = random.randint(0, size_of_child-1)
    index_b = random.randint(0, size_of_child-1)
    child_seq[index_a], child_seq[index_b] = child_seq[index_b], child_seq[index_a]
    child[0] = child_seq
    return child


def verify_if_fit_and_legal(children, l_parent, r_parent, N):
    fit_legal_children = []
    for child in children:
        child_score = child[4]
        child_length = child[3]
        l_parent_score = l_parent[4]
        r_parent_score = r_parent[4]
        #
        if (((child_score > l_parent_score) or (child_score > r_parent_score)) and (child_length <= N)):
            fit_legal_children.append(child)
    return fit_legal_children


def multi_point_crossover(l_parent, r_parent, optimized, l, N):
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
    return children


def survival_of_the_fittest(evaluated_population, size_of_population, N):
    contestants = []
    lottery_picks = get_combination(
        size_of_population, int(size_of_population*0.1))
    for pick in lottery_picks:
        contestants.append([pick, evaluated_population[pick]])
    loser_id = find_worst_seq(contestants, N)
    return loser_id


def mutate(child, optimized, toss, mutation_rate):
    if(toss <= mutation_rate):
        return mutate_by_swap(child)
    elif(toss >= 1-mutation_rate):
        return mutate_by_insertion(child, optimized)
    else: return child


def evolve(population, size_of_population, optimized, mutation_rate, l, N):
    #print(f'worst before: ', min(population, key=lambda x: x[5])[5])
    population = sorted(population, key=lambda x: -x[5])
    population = [p for p in population if p[3] <= N]
    population = population[:(size_of_population//2)]
    generated_children = 0
    iterations = 0
    while len(population) < size_of_population:
        l_parent = population[iterations % len(population)]
        r_parent = population[(iterations+7) % len(population)]
        children = multi_point_crossover(
            l_parent, r_parent, optimized, l, N)
        children = [mutate_by_insertion(c, optimized) for c in children]
        children = map_from_optimized(children, optimized)
        children = evaluate(children, optimized, l, N)
        children = [c for c in children if c[3] <= N]
        population += children
        generated_children += len(children)
        iterations += 1
    #print(f'{generated_children} children generated in {iterations} iterations')
    population = population[:size_of_population]
    #print(f'worst after: ', min(population, key=lambda x: x[5])[5])
    return population

    ## old version
    #pop_children = []
    #for i in range(int(0.25*size_of_population)):
    #    l_parent = tournament(population, size_of_population, N)
    #    r_parent = tournament(population, size_of_population, N)
    #    children = multi_point_crossover(
    #        l_parent, r_parent, optimized, l, N)
    #    for child in children:
    #        child = mutate_by_insertion(child, optimized)
    #        #toss = random.uniform(0, 1)
    #        #if(toss <= mutation_rate):
    #        #    child = mutate_by_swap(child)
    #        #elif(toss >= 1-mutation_rate):
    #        #    child = mutate_by_insertion(child, optimized)
    #    children = map_from_optimized(children, optimized)
    #    children = evaluate(children, optimized, l, N)
    #    children = verify_if_fit_and_legal(children, l_parent, r_parent, N)
    #    if (children):
    #        for child in children:
    #            pop_children.append(child)
    #for child in pop_children:
    #    loser_id = survival_of_the_fittest(
    #        population, size_of_population, N)
    #    population[loser_id] = child


if __name__ == "__main__":
    child = [[1, 2, 3, 4, 5, 6, 7, 8]]
    child = mutate_by_swap(child)
    print(child)

    table = [[9, 10, 20, 30]]
    child = mutate_by_insertion(child, table)
    print(child)
