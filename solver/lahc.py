import numpy as np
from operator import mod
from random import random

class LAHC:
    generator = None
    converger = 0
    converge_step = 0
    checks = 0
    conversion_limit = 100
    curr_best = np.inf
    solution = None

    def set_generator(self, gen):
        self.generator = gen

    def cost_function(self, solution):
        if solution is None:
            return int(round(random()*50))
        return solution.sum().sum()

    def stopping_condition(self, solution):
        if solution is None:
            return False
        self.checks += 1
        new_cost = self.cost_function(solution)
        if new_cost < self.curr_best:
            self.curr_best = new_cost
            self.solution = solution
            self.converger = 0
            self.converge_step = self.checks
        else:
            self.converger += 1
            if self.converger >= self.conversion_limit:
                return True
            else:
                return False

    # TODO: make dis work enzo
    def lahc(self, list_length=10):
        fitness_array = [np.inf] * list_length
        solution = None
        iteration = 0
        while not self.stopping_condition(solution):
            new_sol = None
            counter = 0
            while new_sol is None and counter < 10000:
                print(str(counter), end="\r")
                new_sol = self.generator.generate_random_solution()
                counter += 1
            new_cost = self.cost_function(new_sol)
            virtual_beginning = mod(-iteration, list_length)
            virtual_ending = mod(virtual_beginning + list_length - 1, list_length)
            last_element = fitness_array[virtual_ending]
            if new_cost <= last_element:
                solution = new_sol
            fitness_array[virtual_ending] = self.cost_function(solution)
            iteration += 1

    def get_solution(self):
        return self.solution

