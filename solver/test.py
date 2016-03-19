from generator import Generator
import random as rnd
import pandas as pd
from collections import defaultdict
import time


generator = Generator(demand_bound=6, dmin=1, dmax=7, omin=1, omax=3)


startTime = time.time()
filtered_permutations = generator.generate_all_possible_working_schedules(7)
stopTime = time.time()
print(str(stopTime - startTime))

print("")
print("Filtered permutations:")
for permutation in filtered_permutations:
    print(permutation)
print(str(len(filtered_permutations)) + " valid permutations")

demand = generator.generate_demand(7)
print(demand)

# Navigate the possible work assignments faster
options = defaultdict(list)
for sol in filtered_permutations:
    col = 0
    for col in range(0, len(sol)):
        if sol[col] == 1:
            options[col].append(sol)

random_solution = pd.DataFrame(index=range(0, 7))
curr_col = 0
for curr_col in range(0, len(demand)):
    while not random_solution.sum(axis=1)[curr_col] >= demand[curr_col]:
        new_row = pd.Series(options[curr_col][rnd.randint(0, len(options[curr_col]) - 1)])
        random_solution = pd.concat([random_solution, new_row], axis=1)

print(random_solution.transpose().to_string())


# print(solutions)
