# Standard and third party libraries
import os
import re
from datetime import datetime


def create_results_file():
    now = datetime.now()
    timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    results_file = open("./Results/" + timestamp + ".txt", "a+")
    return results_file


def get_intances():
    instances = os.listdir(".\Instances")
    return instances


def get_spectrum(file):
    spectrum = []
    with open(file, "r") as instance:
        for line in instance:
            spectrum.append(line.strip())
    return spectrum


def set_parameters(instance, spectrum):
    parse_filename = re.findall('[0-9]{3}', instance)
    num_of_oncts_in_org_seq = int(parse_filename[0])
    l = len(spectrum[0])
    N = num_of_oncts_in_org_seq + l - 1
    size_of_spectrum = len(spectrum)
    size_of_population = int(size_of_spectrum/2)
    if(size_of_spectrum < num_of_oncts_in_org_seq):
        perfect_score = size_of_spectrum
    else:
        perfect_score = num_of_oncts_in_org_seq
    return N, l, perfect_score, size_of_population
