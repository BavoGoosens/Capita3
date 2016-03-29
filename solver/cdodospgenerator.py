from generator import Generator
from linked_list import LinkedList
from pandas import DataFrame, Series, concat
from random import randint


class CDODOSPGenerator(Generator):

    x_param = None

    def __init__(self, x_param, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        Generator.__init__(self, demand_bound, dmin, dmax, omin, omax)
        self.x_param = x_param

    def run(self, time_span=7, demand=None):
        self.demand = demand if demand is not None else self.generate_demand(time_span)
        self.time_span = time_span
        schedules = self.generate_working_schedules(time_span)
        return True

    def generate_working_schedules(self, time_span):
        initial_solutions = self.generate_initial_working_schedules(time_span)
        ll = LinkedList()
        self.flatten(initial_solutions, ll)
        filtered_solutions = list()
        for solution in self.possibles:
            if self.is_valid(solution):
                filtered_solutions.append(solution)
        return filtered_solutions

    def generate_random_solution(self):
        random_solution = DataFrame(index=range(0, self.time_span))
        for curr_col in range(0, len(self.demand)):
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                new_row = Series(self.options[curr_col][randint(0, len(self.options[curr_col]) - 1)])
                random_solution = concat([random_solution, new_row], axis=1)
        #print(random_solution.transpose().to_string())
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        return None


