from generator import Generator
from linked_list import LinkedList
import time

possibles = list()

def flatten(element, ll):
        if isinstance(element, list):
            if len(element) == 0:
                res = ll.couple()
                print(res)
            else:
                print("sup")
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


generator = Generator(6, 3, 5, 2, 3)
startTime = time.time()
solutions = generator.generate_solutions(5)
stopTime = time.time()
print str(stopTime-startTime)
ll = LinkedList()

flatten(solutions, ll)


#print(solutions)

