import numpy as np


class LAHC:
    generator = None
    converger = 0
    conversion_limit = 100
    curr_best = np.inf
    solution = None

    def set_generator(self, gen):
        self.generator = gen

    def cost_function(self, solution):
        return solution.sum().sum()

    def stopping_condition(self, solution):
        new_cost = self.cost_function(solution)
        if new_cost < self.curr_best:
            self.curr_best = new_cost
            self.solution = solution
            self.converger = 0
        else:
            self.converger += 1
            if self.converger >= self.conversion_limit:
                return True
            else:
                return False

    # TODO: make dis work enzo
    def lahc(self, list_length=10):
        solution = self.generator.generate_random_solution()
        cost = self.cost_function(solution)
        fitness_array = [99999999999] * list_length
        iteration = 0
        while not self.stopping_condition(solution):
            new_sol = self.generator.generate_random_solution()
            new_cost = self.cost_function(new_sol)
            virtual_beginning = iteration % len(fitness_array)
            if fitness_array[virtual_beginning] >= new_cost:
                solution = new_sol
            else:
                pass
            iteration += 1

    def get_solution(self):
        return self.solution

