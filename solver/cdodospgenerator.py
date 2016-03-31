from generator import Generator
from linked_list import LinkedList
from random import randint
from collections import defaultdict
from pandas import Series, DataFrame, concat
import random as rnd


class CDODOSPGenerator(Generator):
    x_param = None
    option_dict = None
    bad_schedules = None

    def __init__(self, x_param):
        Generator.__init__(self)
        self.x_param = x_param
        self.option_dict = defaultdict(lambda: defaultdict(list))
        self.bad_schedules = list()

    def run(self, time_span=None, dmin=None, dmax=None, omin=None, omax=None, demand=None):
        self.time_span, self.omin, self.omax, self.dmin, self.dmax, self.demand = \
            self.generate_parameters(time_span, omin, omax, dmin, dmax, demand)
        schedules = self.generate_working_schedules()
        if len(schedules) < 2:
            return False
        if self.x_param > len(schedules):
            self.x_param = len(schedules)
        boolean = self.choose_basic_schedules(list(range(0, len(schedules) - 1)), schedules)
        if len(self.option_dict) == 0:
            boolean = False
        return boolean

    def choose_basic_schedules(self, possible_indices, schedules, chosen_indices=list()):
        still_to_be_tried = self.x_param - len(self.option_dict)
        possible_indices = [x for x in possible_indices if x < len(schedules)]
        chosen_indices = []

        for i in range(0, still_to_be_tried):
            # there are no more schedules to be tried
            if len(possible_indices) == 0:
                break
            elif len(possible_indices) == 1:
                possible_index = 0
            else:
                possible_index = randint(0, len(possible_indices) - 1)
            chosen_index = possible_indices[possible_index]
            del possible_indices[possible_index]
            chosen_indices.append(chosen_index)

        # generate the permutations and put them in option_dict
        evaluated_schedules = list()
        for index, schedule_index in enumerate(chosen_indices):
            schedule = schedules[schedule_index]
            permutations = self.generate_permutations(schedule)
            temp_dict = defaultdict(list)
            for permutation in permutations:
                for col in range(0, len(permutation)):
                    if permutation[col] == 1:
                        temp_dict[col].append(permutation)
                        # self.option_dict[index][col].append(permutation)
            ok = True
            for demand_idx, demand in enumerate(self.demand):
                if demand > 0:
                    if demand_idx not in temp_dict:
                        ok = False
                        break
            if ok:
                # Goeie keuze voeg toe aan de dict
                invoeg = len(self.option_dict)
                self.option_dict[invoeg] = temp_dict
            else:
                # Slechte keuze voeg toe aan bad_schedules
                self.bad_schedules.append(schedule_index)
            evaluated_schedules.append(schedule_index)
        # Op dit punt bevat de option dict enkel deftige oplossingen
        # Er kunnen echter nog keuzes mogelijk zijn

        # if there aren't enough perms yet in the final option dict
        # and we know there are unexplored schedules we should try to
        # add more
        if len(self.option_dict) < self.x_param and possible_indices:
            return self.choose_basic_schedules(possible_indices, schedules, [])
        else:
            return True

    def generate_permutations(self, schedule):
        n = len(schedule)
        permutations = [[schedule[i - j] for i in range(n)] for j in range(n)]
        result_list = list()
        for permutation in permutations:
            if self.is_valid(permutation):
                result_list.append(permutation)
        return result_list

    def generate_working_schedules(self):
        initial_solutions = self.generate_initial_working_schedules(self.time_span)
        ll = LinkedList()
        self.flatten(initial_solutions, ll)
        filtered_solutions = list()
        for solution in self.possibles:
            if self.is_valid(solution):
                filtered_solutions.append(solution)
        return filtered_solutions

    def generate_random_solution(self):
        # for key, value in self.option_dict.items():
        #     if len(value) == 0:
        #         del self.option_dict[key]
        chosen_option_index = randint(0, len(self.option_dict) - 1)
        options = self.option_dict[chosen_option_index]
        if len(options) == 0:
            return None
        random_solution = DataFrame(index=range(0, self.time_span))
        indices = list(range(0, len(self.demand)))
        rnd.shuffle(indices)
        for curr_col in indices:
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                if len(options[curr_col]) - 1 > 0:
                    index = randint(0, len(options[curr_col]) - 1)
                else:
                    index = 0
                try:
                    new_row = Series(options[curr_col][index])
                except IndexError:
                    print("Hey")
                random_solution = concat([random_solution, new_row], axis=1)
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        return None
