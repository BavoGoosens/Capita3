import random
import numpy as np

class Generator(object):

    demand_bound = None
    dmin = None
    dmax = None
    omin = None
    omax = None

    def __init__(self, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        self.demand_bound = demand_bound
        self.dmin = dmin
        self.dmax = dmax
        self.omin = omin
        self.omax = omax

    def generate_demand(self, timespan):
        result = list()
        for day in range(0, timespan):
            result.append(random.randint(0, self.demand_bound))
        return result

    def generate_solutions(self, length, last_number=None, consecutive_numbers=0):
        if length == 0:
            return []
        if last_number is None:
            return [0, self.generate_solutions(length-1, 0, 1)], [1, self.generate_solutions(length-1, 1, 1)]
        if last_number == 1:
            if consecutive_numbers < self.dmin:
                return [1, self.generate_solutions(length-1, 1, consecutive_numbers+1)]
            elif consecutive_numbers >= self.dmax:
                return [0, self.generate_solutions(length-1, 0, 1)]
            else:
                return [1, self.generate_solutions(length-1, 1, consecutive_numbers+1)], \
                       [0, self.generate_solutions(length-1, 0, 1)]
        elif last_number == 0:
            if consecutive_numbers < self.omin:
                return [0, self.generate_solutions(length-1, 0, consecutive_numbers+1)]
            elif consecutive_numbers >= self.omax:
                return [1, self.generate_solutions(length-1, 1, 1)]
            else:
                return [0, self.generate_solutions(length-1, 0, consecutive_numbers+1)], \
                       [1, self.generate_solutions(length-1, 1, 1)]

    def is_valid(self, permutation):
        head = permutation[0]
        last = permutation[-1]
        conseqs_head = 0
        conseqs_end = 0
        stop_head = False
        stop_tail = False
        for index, element in enumerate(permutation):
            index = -(index+1)
            element2 = permutation[index]
            if element == head and not stop_head:
                conseqs_head += 1
            else:
                stop_head = True
            if element2 == last and not stop_tail:
                conseqs_end += 1
            else:
                stop_tail = True
            if stop_head and stop_tail:
                break
        if head == 0:
            bool1 = self.omin <= conseqs_head <= self.omax
        else:
            bool1 = self.dmin <= conseqs_head <= self.dmax
        if last == 0:
            bool2 = self.omin <= conseqs_end <= self.omax
        else:
            bool2 = self.dmin <= conseqs_end <= self.dmax
        return bool1 and bool2





