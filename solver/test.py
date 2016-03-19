from generator import Generator
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



# print(solutions)
