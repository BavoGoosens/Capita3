from generator import Generator
from linked_list import LinkedList
from random import randint
from collections import defaultdict
from pandas import Series, DataFrame, concat

class CDODOSPGenerator(Generator):

    x_param = None
    option_dict = None
    bad_schedules = None

    def __init__(self, x_param, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        Generator.__init__(self, demand_bound, dmin, dmax, omin, omax)
        self.x_param = x_param
        self.option_dict = defaultdict(lambda : defaultdict(list))
        self.bad_schedules = list()

    def run(self, time_span=None, dmin=None, dmax=None, omin=None, omax=None, demand=None):
        self.time_span, self.omin, self.omax, self.dmin, self.dmax, self.demand = \
            self.generate_parameters(time_span, omin, omax, dmin, dmax, demand)
        schedules = self.generate_working_schedules(time_span)
        if len(schedules) < 2:
            return False
        return self.choose_basic_schedules(list(range(0, len(schedules))), schedules)

    def choose_basic_schedules(self, possible_indices, schedules, chosen_indices=list(), wrong_idx=-1):
        #if len(possible_indices) == 0:
        #    return False

        if wrong_idx > -1:
            if len(possible_indices) == 0:
                    return False
            elif len(possible_indices) == 1:
                possible_index = 0
            else:
                possible_index = randint(0, len(possible_indices)-1)
            chosen_index = possible_indices[possible_index]
            del possible_indices[possible_index]
            chosen_indices[wrong_idx] = chosen_index
        else:
            for i in range(0, self.x_param):
                if len(possible_indices) == 0:
                    return False
                elif len(possible_indices) == 1:
                    possible_index = 0
                else:
                    possible_index = randint(0, len(possible_indices)-1)
                chosen_index = possible_indices[possible_index]
                del possible_indices[possible_index]
                chosen_indices.append(chosen_index)

        for index, schedule_index in enumerate(chosen_indices):
            schedule = schedules[schedule_index]
            permutations = self.generate_permutations(schedule)
            for permutation in permutations:
                for col in range(0, len(permutation)):
                    if permutation[col] == 1:
                        self.option_dict[index][col].append(permutation)
        for option_idx, value in self.option_dict.items():
            for demand_idx, demand in enumerate(self.demand):
                if demand > 0:
                    if demand_idx not in value:
                        self.bad_schedules.append(chosen_indices[option_idx])
                        self.option_dict = defaultdict(lambda : defaultdict(list))
                        return self.choose_basic_schedules(possible_indices, schedules, chosen_indices, option_idx)
        return True

    def generate_permutations(self, schedule):
        print("Generating permutations...")
        n = len(schedule)
        permutations = [[schedule[i - j] for i in range(n)] for j in range(n)]
        result_list = list()
        for permutation in permutations:
            if self.is_valid(permutation):
                result_list.append(permutation)
        return result_list

    def generate_working_schedules(self, time_span):
        print("Generating working schedules...")
        initial_solutions = self.generate_initial_working_schedules(time_span)
        ll = LinkedList()
        self.flatten(initial_solutions, ll)
        filtered_solutions = list()
        for solution in self.possibles:
            if self.is_valid(solution):
                filtered_solutions.append(solution)
        return filtered_solutions

    def generate_random_solution(self):
        chosen_option_index = randint(0, self.x_param-1)
        options = self.option_dict[chosen_option_index]
        random_solution = DataFrame(index=range(0, self.time_span))
        for curr_col in range(0, len(self.demand)):
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                new_row = Series(options[curr_col][randint(0, len(options[curr_col]) - 1)])
                random_solution = concat([random_solution, new_row], axis=1)
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        return None



