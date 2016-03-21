from solutiongenerator import SolutionGenerator
import random as rnd
import pandas as pd
from collections import defaultdict
import time


generator = SolutionGenerator(demand_bound=6, dmin=1, dmax=7, omin=1, omax=3)
demand = [3, 3, 3, 3, 3, 2, 2]
generator.run(7, demand)

solution = generator.generate_random_solution()
# TODO: Mickey check of ge de refactor goed vindt :D
#
# startTime = time.time()
# filtered_permutations = generator.generate_all_possible_working_schedules(7)
# stopTime = time.time()
# print(str(stopTime - startTime))
#
# print("")
# print("Filtered permutations:")
# for permutation in filtered_permutations:
#     print(permutation)
# print(str(len(filtered_permutations)) + " valid permutations")
#
# # demand = generator.generate_demand(7)
# demand = [3,3,3,3,3,2,2]
# print(demand)
#
# # Navigate the possible work assignments faster
# options = defaultdict(list)
# for sol in filtered_permutations:
#     col = 0
#     for col in range(0, len(sol)):
#         if sol[col] == 1:
#             options[col].append(sol)
#
# random_solution = pd.DataFrame(index=range(0, 7))
# curr_col = 0
# for curr_col in range(0, len(demand)):
#     while not random_solution.sum(axis=1)[curr_col] >= demand[curr_col]:
#         new_row = pd.Series(options[curr_col][rnd.randint(0, len(options[curr_col]) - 1)])
#         random_solution = pd.concat([random_solution, new_row], axis=1)
#
# print(random_solution.transpose().to_string())

# Can be used to quickly check which solutions were already tried
# fst_sum = random_solution.sum(axis=0)
# snd_sum = random_solution.sum(axis=1)
# id = ""
# for sum in fst_sum:
#     id += str(sum)
# for sum in snd_sum:
#     id += str(sum)
# print(id)


# print(solutions)
