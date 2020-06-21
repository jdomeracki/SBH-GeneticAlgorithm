# Standard and third party libraries
import random
import os
from math import *
from itertools import combinations
from operator import itemgetter
from timeit import default_timer as timer

# Local modules
from io_handler import *
from preliminary_optimization import *
from population_generator import *
from evolution import *

if __name__ == "__main__":
    results_file = create_results_file()
    instances = get_intances()
    modes = ['append', 'prepend']
    for instance in instances:
        spectrum = get_spectrum("./Instances/" + instance)
        results_file.write(instance + "\n")
        print(instance)
        N, l, perfect_score, size_of_population = set_parameters(
            instance, spectrum)
        current_best = None
        start = timer()
        optimized = optimize(spectrum, modes[1])
        pre_check = check_if_perfect(optimized, N)
        if(pre_check >= 0):
            optimal = optimized[pre_check]
            results_file.write("Length: " + str(len(optimal)) + " Score: " +
                               str(perfect_score) + " Accuracy: 100%")
        else:
            inital_population = generate_population(
                optimized, size_of_population, N)
            evaluated_population = evaluate(inital_population, optimized, l, N)
            current_best = get_best_seq(evaluated_population, N)
            results_file.write("Generation: 1 ")
            results_file.write("Length: " + str(current_best[3]) + " Score: " + str(
                current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%\n")
            evolve(evaluated_population, size_of_population, optimized, N, l)
            current_best = get_best_seq(evaluated_population, N)
            results_file.write("Generation: " + str(size_of_population*0.9))
            results_file.write(" Length: " + str(current_best[3]) + " Score: " + str(
                current_best[4]) + " Accuracy: " + str((current_best[4]/perfect_score)*100) + "%")
        end = timer()
        results_file.write(" Execution time: " + str(end - start) + " [s]\n")
        print("Execution time: " + str(end - start) + " [s]\n")
