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


if __name__ == "__main__":
    results_file = create_results_file()
    instances = get_intances()
    modes = ['append', 'prepend']
    for instance in instances:
        spectrum = get_spectrum(
            "./Instances/RepetitionNegativeErrors/" + instance)
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
            optimized_elements, size_of_population, N)
        evaluated_population = evaluate(
            inital_population, optimized_elements, l, N)
        current_best = get_best_seq(evaluated_population, N)
        print(current_best)
        results_file.write("Generation: 1 ")
        results_file.write("Length: " + str(current_best[3]) + " Score: " + str(
            current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%\n")
        evolve(evaluated_population, size_of_population,
               optimized_elements, N, l)
        current_best = get_best_seq(evaluated_population, N)
        print(current_best)
        results_file.write("Generation: 100")  # + str(size_of_population*0.9))
        results_file.write(" Length: " + str(current_best[3]) + " Score: " + str(
            current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%")
        end = timer()
        # accuracy_list.append((current_best[4]/perfect_score)*100)
        results_file.write(" Execution time: " + str(end - start) + " [s]\n")
        print("Execution time: " + str(end - start) + " [s]\n")
