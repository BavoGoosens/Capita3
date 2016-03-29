import sys
import argparse
from lahc import LAHC
from solutiongenerator import SolutionGenerator

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timespan",
                    help="The timespan you wish to make a planning for", type=int)
parser.add_argument('-d', '--demand',
                    help='delimited list input with the demand for each day',
                    type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument("--offdaymin",
                    help="The minimum amount of consecutive off/free days  an employee needs to receive", type=int)
parser.add_argument("--offdaymax",
                    help="The maximum amount of consecutive off/free days an employee could receive", type=int)
parser.add_argument("--ondaymin",
                    help="The minimum amount of consecutive on/work days an employee needs to receive", type=int)
parser.add_argument("--ondaymax",
                    help="The minimum amount of consecutive on/work days an employee could receive", type=int)
args = parser.parse_args()


def main(argv):
    print("Welcome to this solver :) \n \n")
    # Read the supplied command line arguments
    timespan = args.timespan
    offdaysmin = args.offdaymin
    offdaysmax = args.offdaymax
    ondaysmin = args.ondaymin
    ondaysmax = args.ondaymax
    demand = args.demand
    # Set some default values
    if timespan is None:
        timespan = 7
    if offdaysmin is None:
        offdaysmin = 1
    if offdaysmax is None:
        offdaysmax = 2
    if ondaysmin is None:
        ondaysmin = 1
    if ondaysmax is None:
        ondaysmax = 4
    # TODO: merge everything from test
    generator = SolutionGenerator(demand_bound=6, dmin=ondaysmin, dmax=ondaysmax, omin=offdaysmin, omax=offdaysmax)
    generator.run(timespan, demand)
    demand = generator.demand

    if len(demand) < timespan or len(demand) > timespan:
        print("There was an issue with the array of demand values. "
              "Make sure it is exactly as long as the timespan you provided! "
              "We'll just use random values otherwise. \n")
        return

    s = LAHC()
    s.set_generator(generator)
    s.lahc(10)
    sol = s.get_solution()

    print("\n\n*********** SOLUTION ***********\n")
    print("Overview:" + "\n>> timespan: " + str(timespan) +
          "\n>> demand for the timespan: " + str(demand) +
          "\n>> min number of free days: " + str(offdaysmin) +
          "\n>> max number of free days: " + str(offdaysmax) +
          "\n>> min number of work days: " + str(ondaysmin) +
          "\n>> max number of work days: " + str(ondaysmax)+"\n\n")
    print(sol.to_string())

if __name__ == "__main__":
    main(sys.argv[1:])
