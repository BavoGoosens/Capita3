import sys
import random as rnd
from cdodospgenerator import CDODOSPGenerator
from gdodospgenerator import GDODOSPGenerator

def main():
    dummy = [5, 7, 14]
    timespan = dummy[rnd.randint(0, len(dummy) - 1)]
    offdaysmin = rnd.randint(0, timespan)
    if offdaysmin == 0:
        offdaysmax = rnd.randint(1, timespan)
    else:
        offdaysmax = rnd.randint(offdaysmin, timespan)
    ondaysmin = rnd.randint(0, timespan)
    if ondaysmin == 0:
        ondaysmax = rnd.randint(1, timespan)
    else:
        ondaysmax = rnd.randint(ondaysmin, timespan)

    generator = GDODOSPGenerator(demand_bound=2*timespan, dmin=ondaysmin, dmax=ondaysmax, omin=offdaysmin, omax=offdaysmax)
    success = generator.run(timespan)


if __name__ == "__main__":
    main(sys.argv[1:])