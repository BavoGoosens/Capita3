import pandas as pd
import random as rnd

from linked_list import LinkedList
from generator import Generator


class GDODOSPGenerator(Generator):

    def run(self, time_span=7, demand=None):
        self.demand = demand if demand is not None else self.generate_demand(time_span)
        self.time_span = time_span
        schedules = self.generate_working_schedules(time_span)
        self.filter_and_set_options(schedules)

        for index, demand_day in enumerate(self.demand):
            if demand_day > 0:
                if index not in self.options.keys():
                    return False
        if len(self.options) < 2:
            return False
        return True

    def generate_working_schedules(self, time_span):
        initial_solutions = self.generate_initial_working_schedules(time_span)
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
        random_solution = pd.DataFrame(index=range(0, self.time_span))
        for curr_col in range(0, len(self.demand)):
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                new_row = pd.Series(self.options[curr_col][rnd.randint(0, len(self.options[curr_col]) - 1)])
                random_solution = pd.concat([random_solution, new_row], axis=1)
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        return None
