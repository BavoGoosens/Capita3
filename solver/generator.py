from collections import defaultdict
from random import randint
from linked_list import LinkedList

import numpy as np


class Generator(object):

    demand_bound = None
    dmin = None
    dmax = None
    omin = None
    omax = None

    options = None
    time_span = None
    demand = None

    number_of_different_solutions = None

    possibles = None
    already_generated = None

    def __init__(self, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        self.demand_bound = demand_bound
        self.dmin = dmin
        self.dmax = dmax
        self.omin = omin
        self.omax = omax
        self.options = defaultdict(list)
        self.possibles = list()
        self.already_generated = list()

    def generate_demand(self, time_span):
        result = list()
        for day in range(0, time_span):
            result.append(randint(0, self.demand_bound))
        return result

    def get_number_of_different_solutions(self):
        if self.number_of_different_solutions is None:
            self.number_of_different_solutions = 0
            for index, demand_day in enumerate(self.demand):
                number_of_options = len(self.options[index])
                power = pow(demand_day, number_of_options)
                self.number_of_different_solutions += power
        return self.number_of_different_solutions

    def filter_and_set_options(self, options):
        for option in options:
            for col in range(0, len(option)):
                if option[col] == 1:
                    self.options[col].append(option)

    def generate_initial_working_schedules(self, length, last_number=None, consecutive_numbers=0):
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

    def generate_solution_id(self, solution):
        thing = solution.values
        larger = ""
        for t in thing:
            larger += str(t)
        larger = larger.replace(' ', '').replace('[', '').replace(']', '').replace('\n', '')
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