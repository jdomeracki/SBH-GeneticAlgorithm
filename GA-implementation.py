# Standard and third party libraries
import random
import os
import numpy as np
from math import *
from itertools import combinations
from operator import itemgetter
from timeit import default_timer as timer
from matplotlib import pyplot as plt

# Local modules
from io_handler import *
from preliminary_optimization import *
from population_generator import *
from evolution import *
from data_visualization import *

MUTATION_RATE = 0.1

if __name__ == "__main__":
    results_file = create_results_file()
    problem_types = ['RandomPositiveErrors', 'RandomNegativeErrors',
                    'PositiveErrorsWithDistortions', 'NegativeByRepetition']
    problem_type = problem_types[2]
    instances = get_intances(problem_type)
    for instance in instances:
        spectrum = get_spectrum(
            "./Instances/" + problem_type + "/" + instance)
        results_file.write(instance + "\n")
        print(instance)
        N, l, perfect_score, size_of_population, size_of_spectrum = set_parameters(
            instance, spectrum)
        current_best = None
        start = timer()
        optimized_elements = optimization(spectrum, size_of_spectrum)
        best_post_opt_key = max(optimized_elements,
                                key=lambda x: len(optimized_elements[x]))
        inital_population = generate_population(
            optimized_elements, size_of_population, best_post_opt_key, N)
        evaluated_population = evaluate(
            inital_population, optimized_elements, l, N)
        best_found = find_best_seq(evaluated_population, N)
        print(best_found)
        # results_file.write("Generation: 1 ")
        # results_file.write("Length: " + str(current_best[3]) + " Score: " + str(
        #    current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%\n")
        counter = 0
        generations = 1
        max_turns_without_change = 10
        while(counter < max_turns_without_change):
            generations += 1
            evaluated_population = evolve(evaluated_population, size_of_population,
                   optimized_elements, MUTATION_RATE, l, N)
            #current_best = find_best_seq(evaluated_population, N)
            current_best = max(evaluated_population, key=lambda x: x[5])
            if(current_best[5] > best_found[5]):
                best_found = current_best
                # print(best_found)
                counter = 0
            else:
                counter += 1
                if counter == max_turns_without_change:
                    print(f'{max_turns_without_change} turns without change...')
        print(generations)
        print(best_found)
        # results_file.write("Generation: 100")  # + str(size_of_population*0.9))
        # results_file.write(" Length: " + str(current_best[3]) + " Score: " + str(
        #   current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%")
        end = timer()
        # accuracy_list.append((current_best[4]/perfect_score)*100)
        results_file.write(" Execution time: " + str(end - start) + " [s]\n")
        print("Execution time: " + str(end - start) + " [s]\n")
        break
