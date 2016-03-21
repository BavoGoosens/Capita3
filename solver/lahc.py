import numpy as np

generator = None

def set_generator(gen):
    global generator
    generator = gen

# TODO: make dis work enzo
def lahc(list_length=10):
    initial_solution = generator.generate_random_solution()
    cost = cost_function(initial_solution)
    fitness_array = [np.inf] * list_length
    iteration = 0
    virtual_beginning = 0
    while (stopping condition not satisfied):
        new_sol = construct_candidate_solution()
        new_cost = cost_function(new_sol)
        virtual_beginning = divmod(iteration, len(fitness_array))
        if new_cost <= fitness_array[virtual_beginning]:
            accept candidate
        else:
            reject_candidate

        iteration += 1
