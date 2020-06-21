# Standard and third party libraries
from math import *
from itertools import combinations
import random

# Local modules
from population_generator import evaluate, get_combination


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


def evolve(population, size_of_population, optimized, N, l):
    for i in range(int(0.9*size_of_population)):
        pop_children = []
        for i in range(int(0.25*size_of_population)):
            l_parent = tournament(population, size_of_population, N)
            r_parent = tournament(population, size_of_population, N)
            children = multi_point_crossover(
                l_parent, r_parent, optimized, l, N)
            for child in children:
                pop_children.append(child)
        for child in pop_children:
            loser_id = survival_of_the_fittest(
                population, size_of_population, N)
            population[loser_id] = child
