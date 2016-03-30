import pandas as pd
import random as rnd

from linked_list import LinkedList
from generator import Generator


class GDODOSPGenerator(Generator):

    def run(self, time_span=None, dmin=None, dmax=None, omin=None, omax=None, demand=None):
        self.time_span, self.omin, self.omax, self.dmin, self.dmax, self.demand = \
            self.generate_parameters(time_span, omin, omax, dmin, dmax, demand)
        schedules = self.generate_working_schedules()
        self.filter_and_set_options(schedules)

        for index, demand_day in enumerate(self.demand):
            if demand_day > 0:
                if index not in self.options.keys():
                    return False
        if len(self.options) < 2:
            return False
        return True

    def generate_working_schedules(self):
        initial_solutions = self.generate_initial_working_schedules(self.time_span)
        ll = LinkedList()
        self.flatten(initial_solutions, ll)
        filtered_solutions = list()
        for solution in self.possibles:
            if self.is_valid(solution):
                filtered_solutions.append(solution)
        permutations = list()
        for a in filtered_solutions:
            n = len(a)
            permutations.append([[a[i - j] for i in range(n)] for j in range(n)])
        filtered_permutations = list()
        for permutation_row in permutations:
            for permutation in permutation_row:
                if permutation not in filtered_permutations and self.is_valid(permutation):
                    filtered_permutations.append(permutation)
        filtered_permutations = filtered_permutations
        return filtered_permutations

    def generate_random_solution(self):
        if len(self.already_generated) == self.get_number_of_different_solutions():
            return True
        random_solution = pd.DataFrame(index=range(0, self.time_span))
        self.get_number_of_different_solutions()
        indices = list(range(0, len(self.demand)))
        rnd.shuffle(indices)
        for curr_col in indices:
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                random_index = rnd.randint(0, len(self.options[curr_col]) - 1)
                new_row = pd.Series(self.options[curr_col][random_index])
                random_solution = pd.concat([random_solution, new_row], axis=1)
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        return None
