import sys
import argparse
import random as rnd
from lahc import LAHC
from gdodospgenerator import GDODOSPGenerator
from cdodospgenerator import CDODOSPGenerator

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timespan",
                    help="The timespan you wish to make a planning for", type=int)
parser.add_argument('-d', '--demand',
                    help='delimited list input with the demand for each day',
                    type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument("-l", "--listlength",
                    help="The list length used by the LAHC algorithm")
parser.add_argument("-x", "--xparam",
                    help="The number of neighbourhoods to be considered (only useful when using cdodosp)")
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
    #print("\nWelcome to this solver :)\n")
    # Read the supplied command line arguments
    timespan = args.timespan
    offdaysmin = args.offdaymin
    offdaysmax = args.offdaymax
    ondaysmin = args.ondaymin
    ondaysmax = args.ondaymax
    demand = args.demand

    list_length = args.listlength
    x_param = args.xparam

    if list_length is None:
        list_length = 10
    else:
        list_length = int(list_length)
    if x_param is None:
        x_param = 10

    success = False
    while not success:
        generator = GDODOSPGenerator()
        success = generator.run(timespan, ondaysmin, ondaysmax, offdaysmin, offdaysmax, demand)
        if not success:
            timespan = None
            offdaysmin = None
            offdaysmax = None
            ondaysmin = None
            ondaysmax = None
            #print("Problem not solvable. Creating new random problem.")

    demand = generator.demand

    print("\n\n*********** SOLUTION ***********\n")
    print("Overview:" + "\n>> timespan: " + str(generator.time_span) +
          "\n>> demand for the timespan: " + str(generator.demand) +
          "\n>> min number of free days: " + str(generator.omin) +
          "\n>> max number of free days: " + str(generator.omax) +
          "\n>> min number of work days: " + str(generator.dmin) +
          "\n>> max number of work days: " + str(generator.dmax)+"\n\n")

    if len(demand) < generator.time_span or len(demand) > generator.time_span:
        #print("There was an issue with the array of demand values. "
        #      "Make sure it is exactly as long as the timespan you provided! "
        #      "We'll just use random values otherwise. \n")
        return

    s = LAHC()
    s.set_generator(generator)
    s.lahc(list_length)
    sol = s.get_solution()
    print(sol.to_string())
    print(s.curr_best)
    #print("\nConverged after "+str(s.converge_step)+" iterations")
if __name__ == "__main__":
    main(sys.argv[1:])
