import random
from collections import defaultdict

import numpy as np
import pandas as pd
import random as rnd

from linked_list import LinkedList
from math import pow


class SolutionGenerator(object):
    options = defaultdict(list)
    possibles = list()
    already_generated = list()
    demand_bound = None
    demand = list()
    dmin = None
    dmax = None
    omin = None
    omax = None
    time_span = 0
    recursive_calls = 0
    number_of_different_solutions = 0

    def __init__(self, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        self.demand_bound = demand_bound
        self.dmin = dmin
        self.dmax = dmax
        self.omin = omin
        self.omax = omax

    def run(self, time_span=7, demand=None):
        filtered_permutations = self.generate_all_possible_working_schedules(time_span)

        if demand is None:
            self.demand = self.generate_demand(time_span)
        else:
            self.demand = demand

        self.time_span = time_span

        # Navigate the possible work assignments faster

        for sol in filtered_permutations:
            for col in range(0, len(sol)):
                if sol[col] == 1:
                    self.options[col].append(sol)
        for index, demand_day in enumerate(self.demand):
            if demand_day > 0:
                if index not in self.options.keys():
                    return False

        self.set_number_of_different_solutions()

        if len(self.options) < 2:
            print("Not enough permutations...")
            return False

        return True

    def generate_demand(self, time_span):
        result = list()
        for day in range(0, time_span):
            result.append(random.randint(0, self.demand_bound))
        return result

    def set_number_of_different_solutions(self):
        self.number_of_different_solutions = 0
        for index, demand_day in enumerate(self.demand):
            number_of_options = len(self.options[index])
            power = pow(demand_day, number_of_options)
            self.number_of_different_solutions += power

    def generate_initial_working_schedules(self, length, last_number=None, consecutive_numbers=0):
        self.recursive_calls += 1
        #if self.recursive_calls % 1000000 == 0:
        #    print(str(self.recursive_calls)+" recursive calls")
        #sys.stdout.flush()
        if length == 0:
            return []
        if last_number is None:
            return [0, self.generate_initial_working_schedules(length - 1, 0, 1)], \
                   [1, self.generate_initial_working_schedules(length - 1, 1, 1)]
        if last_number == 1:
            if consecutive_numbers < self.dmin:
                return [1, self.generate_initial_working_schedules(length - 1, 1, consecutive_numbers + 1)]
            elif consecutive_numbers >= self.dmax:
                return [0, self.generate_initial_working_schedules(length - 1, 0, 1)]
            else:
                return [1, self.generate_initial_working_schedules(length - 1, 1, consecutive_numbers + 1)], \
                       [0, self.generate_initial_working_schedules(length - 1, 0, 1)]
        elif last_number == 0:
            if consecutive_numbers < self.omin:
                return [0, self.generate_initial_working_schedules(length - 1, 0, consecutive_numbers + 1)]
            elif consecutive_numbers >= self.omax:
                return [1, self.generate_initial_working_schedules(length - 1, 1, 1)]
            else:
                return [0, self.generate_initial_working_schedules(length - 1, 0, consecutive_numbers + 1)], \
                       [1, self.generate_initial_working_schedules(length - 1, 1, 1)]

    def generate_all_possible_working_schedules(self, time_span):
        print("Calculating initial solutions... This might take a while.")
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
        curr_col = 0
        for curr_col in range(0, len(self.demand)):
            while not random_solution.sum(axis=1)[curr_col] >= self.demand[curr_col]:
                new_row = pd.Series(self.options[curr_col][rnd.randint(0, len(self.options[curr_col]) - 1)])
                random_solution = pd.concat([random_solution, new_row], axis=1)

        #print(random_solution.transpose().to_string())
        solution_id = self.generate_solution_id(random_solution)
        if solution_id not in self.already_generated:
            self.already_generated.append(solution_id)
            return random_solution.transpose()
        else:
            return None

    def generate_solution_id(self, solution):
        thing = solution.values
        larger = ""
        for t in thing:
            larger += str(t)
        larger = larger.replace(' ', '').replace('[', '').replace(']', '')
        fingerprint = int(larger, 2)
        return fingerprint

    def is_valid(self, permutation):
        max_conseq_ones = 0
        min_conseq_ones = np.inf
        max_conseq_zeros = 0
        min_conseq_zeros = np.inf
        conseq_ones = 0
        conseq_zeros = 0
        previous_element = None
        for element in permutation:
            if element == 0:
                conseq_zeros += 1
            else:
                conseq_ones += 1
            if previous_element is not None and element != previous_element:
                if previous_element == 1:
                    if max_conseq_ones < conseq_ones:
                        max_conseq_ones = conseq_ones
                    if min_conseq_ones > conseq_ones:
                        min_conseq_ones = conseq_ones
                    conseq_ones = 0
                else:
                    if max_conseq_zeros < conseq_zeros:
                        max_conseq_zeros = conseq_zeros
                    if min_conseq_zeros > conseq_zeros:
                        min_conseq_zeros = conseq_zeros
                    conseq_zeros = 0
            previous_element = element

        if max_conseq_ones < conseq_ones:
            max_conseq_ones = conseq_ones
        if min_conseq_ones > conseq_ones > 0:
            min_conseq_ones = conseq_ones
        if max_conseq_zeros < conseq_zeros:
            max_conseq_zeros = conseq_zeros
        if min_conseq_zeros > conseq_zeros > 0:
            min_conseq_zeros = conseq_zeros
        bool1 = min_conseq_zeros >= self.omin
        bool2 = max_conseq_zeros <= self.omax
        bool3 = min_conseq_ones >= self.dmin
        bool4 = max_conseq_ones <= self.dmax
        return bool1 and bool2 and bool3 and bool4

    def flatten(self, element, ll):
        if isinstance(element, list):
            if len(element) == 0:
                res = ll.couple()
                self.possibles.append(res)
            else:
                head = element[0]
                tail = element[1]
                ll.add(head)
                self.flatten(tail, ll)
        elif isinstance(element, tuple):
            # splits de linked list
            fst = element[0]
            snd = element[1]
            newll1 = LinkedList(ll)
            newll2 = LinkedList(ll)
            self.flatten(fst, newll1)
            self.flatten(snd, newll2)
        elif isinstance(element, int):
            ll.add(element)
