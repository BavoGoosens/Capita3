from generator import Generator

class CDODOSPGenerator(Generator):

    x_param = None

    def __init__(self, x_param, demand_bound=6, dmin=1, dmax=3, omin=1, omax=2):
        Generator.__init__(self, demand_bound, dmin, dmax, omin, omax)
        self.x_param = x_param

    def run(self, time_span=7, demand=None):
        schedules = self.generate_working_schedules()


