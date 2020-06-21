# Standard and third party libraries
from math import *


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


def find_match(spectrum, mode):
    # random.shuffle(spectrum)
    toss = 1
    if(mode == 'append'):
        for i in range(len(spectrum)):
            for j in range(i+1, len(spectrum)):
                match = perfect_match(spectrum[i], spectrum[j])
                #toss = random.uniform(0, 1)
                if(match and toss <= 1):
                    spectrum.pop(j)
                    spectrum.pop(i)
                    spectrum.append(match)
                    return spectrum
    elif(mode == 'prepend'):
        for i in range(len(spectrum)):
            for j in range(i+1, len(spectrum)):
                match = perfect_match(spectrum[i], spectrum[j])
                #toss = random.uniform(0, 1)
                if(match and toss <= 1):
                    spectrum.pop(j)
                    spectrum.pop(i)
                    spectrum.insert(0, match)
                    return spectrum
    return []


def list_to_dict(lst):
    dct = {i: lst[i] for i in range(0, len(lst))}
    return dct


def optimize(spectrum, mode):
    optimized = []
    while(True):
        current = find_match(spectrum, mode)
        if(current):
            optimized = current
        else:
            break
    optimized = list_to_dict(optimized)
    return optimized


def check_if_perfect(optimized, N):
    for k in optimized:
        if(len(optimized[k]) == N):
            return k
    return -1
