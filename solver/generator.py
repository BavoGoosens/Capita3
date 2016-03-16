import random


class Generator(object):
    demand_bound = None

    def __init__(self, demand_bound=6):
        self.demand_bound = demand_bound

    def generate_demand(self, timespan):
        result = list()
        for day in range(0, timespan):
            result.append(random.randint(0, self.demand_bound))
        return result
