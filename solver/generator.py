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
        max_conseq_ones = 0
        min_conseq_ones = np.inf
        max_conseq_zeros = 0
        min_conseq_zeros = np.inf
        conseq_ones = 0
        conseq_zeros = 0
        previous_element = None
        for element in permutation:
            if previous_element is not None:
                if element == previous_element:
                    if element == 0:
                        conseq_zeros += 1
                    else:
                        conseq_ones += 1
                else:
                    if previous_element == 1:
                        if max_conseq_ones < conseq_ones:
                            max_conseq_ones = conseq_ones
                        if min_conseq_ones > conseq_ones:
                            min_conseq_ones = conseq_ones
                        conseq_zeros = 1
                    else:
                        if max_conseq_zeros < conseq_zeros:
                            max_conseq_zeros = conseq_zeros
                        if min_conseq_zeros > conseq_zeros:
                            min_conseq_zeros = conseq_zeros
                        conseq_ones = 1
            else:
                if element == 1:
                    conseq_ones = 1
                else:
                    conseq_zeros = 1
            previous_element = element
        if max_conseq_ones < conseq_ones:
            max_conseq_ones = conseq_ones
        if min_conseq_ones > conseq_ones:
            min_conseq_ones = conseq_ones
        if max_conseq_zeros < conseq_zeros:
            max_conseq_zeros = conseq_zeros
        if min_conseq_zeros > conseq_zeros:
            min_conseq_zeros = conseq_zeros
        bool1 = min_conseq_zeros >= self.omin
        bool2 = max_conseq_zeros <= self.omax
        bool3 = min_conseq_ones >= self.dmin
        bool4 = max_conseq_ones <= self.dmax
        return bool1 and bool2 and bool3 and bool4





