from generator import Generator
from linked_list import LinkedList
import time

possibles = list()

def flatten(element, ll):
        if isinstance(element, list):
            if len(element) == 0:
                res = ll.couple()
                possibles.append(res)
            else:
                head = element[0]
                tail = element[1]
                ll.add(head)
                flatten(tail, ll)
        elif isinstance(element, tuple):
            # splits de linked list
            fst = element[0]
            snd = element[1]
            newll1 = LinkedList(ll)
            newll2 = LinkedList(ll)
            flatten(fst, newll1)
            flatten(snd, newll2)
        elif isinstance(element, int):
            ll.add(element)


generator = Generator(demand_bound=6, dmin=1, dmax=7, omin=1, omax=3)
startTime = time.time()
solutions = generator.generate_solutions(7)
stopTime = time.time()
print(str(stopTime-startTime))
ll = LinkedList()
flatten(solutions, ll)
filtered_solutions = list()
for solution in possibles:
    if generator.is_valid(solution):
        filtered_solutions.append(solution)
permutations = list()
for a in filtered_solutions:
    n = len(a)
    permutations.append([[a[i - j] for i in range(n)] for j in range(n)])

filtered_permutations = list()
for permutation_row in permutations:
    for permutation in permutation_row:
        if permutation not in filtered_permutations and generator.is_valid(permutation):
            filtered_permutations.append(permutation)
filtered_permutations = filtered_permutations
print("")
print("Filtered permutations:")
for permutation in filtered_permutations:
    print(permutation)
print(str(len(filtered_permutations))+" valid permutations")



#print(solutions)

