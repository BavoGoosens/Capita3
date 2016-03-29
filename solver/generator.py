from collections import defaultdict


class Generator(object):

    demand_bound = None
    dmin = None
    dmax = None
    omin = None
    omax = None

    options = None

    def __init__(self, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        self.demand_bound = demand_bound
        self.dmin = dmin
        self.dmax = dmax
        self.omin = omin
        self.omax = omax
        self.options = defaultdict(list)