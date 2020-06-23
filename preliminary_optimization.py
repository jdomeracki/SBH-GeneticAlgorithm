# Standard and third party libraries


def create_overlay_matrix(n):
    matrix = [[0]*n for i in range(n)]
    return matrix


def perfect_match(l_o_nct, r_o_nct):
    r = len(r_o_nct)
    if (l_o_nct[1:] == r_o_nct[:r-1]):
        return True
    else:
        return False


def matching_indexes(l_sublist, r_sublist):
    if (l_sublist[-1] == r_sublist[0]):
        return True
    else:
        return False


def fill_the_matrix(matrix, spectrum, n):
    for i in range(n):
        for j in range(n):
            if(i == j):
                continue
            else:
                if(perfect_match(spectrum[i], spectrum[j])):
                    matrix[i][j] = 1
    return matrix


def optimize(filled_matrix, n):
    eliminated_columns = []
    matching_pairs = []
    for i in range(n):
        if(sum(filled_matrix[i]) == 1):
            tmp_index = -1
            tmp_sum = -1
            for j in range(n):
                if(filled_matrix[i][j] == 1):
                    tmp_index = j
                    break
            if(tmp_index in eliminated_columns):
                break
            else:
                for k in range(n):
                    tmp_sum += filled_matrix[k][tmp_index]
                if(tmp_sum == 0):
                    matching_pairs.append([i, tmp_index])
                else:
                    eliminated_columns.append(tmp_index)
    return matching_pairs


def find_match(elements):
    for i in range(len(elements)):
        for j in range(i, len(elements)):
            match = matching_indexes(elements[i], elements[j])
            if(match):
                l = elements[i]
                r = elements[j]
                elements.pop(j)
                elements.pop(i)
                elements.insert(0, l[:-1] + r)
                return elements
    return []


def list_to_dict(lst):
    dct = {i: lst[i] for i in range(0, len(lst))}
    return dct


def accumulate_matching(elements, spectrum, N):
    optimized = []
    while(True):
        current = find_match(elements)
        if(current):
            optimized = elements
        else:
            break
    ambigous = []
    for i in range(N):
        if(not(any(i in element for element in elements))):
            ambigous.append(i)
    for amb_elem in ambigous:
        elements.append([amb_elem])
    seqs = []
    for element in elements:
        seq = spectrum[element[0]]
        for i in range(1, len(element)):
            seq += spectrum[element[i]][-1]
        seqs.append(seq)
    optimized = list_to_dict(seqs)
    return optimized


def optimization(spectrum, N):
    perfect_overlay_matrix = create_overlay_matrix(N)
    filled_matrix = fill_the_matrix(perfect_overlay_matrix, spectrum, N)
    distinct_matches = optimize(filled_matrix, N)
    optimized_elements = accumulate_matching(distinct_matches, spectrum, N)
    return optimized_elements
