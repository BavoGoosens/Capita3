from generator import Generator
from linked_list import LinkedList

def flatten(element, ll):
    for el in element:
        if isinstance(el, list):
            print("sup")
            flatten(el, ll)
        elif isinstance(el, tuple):
            element[0]
            element[1]
        elif isinstance(el, int):
            ll.add(el)
    return ll

generator = Generator(6, 3, 5, 2, 3)
solutions = generator.generate_solutions(5)
ll = LinkedList()

flatten(solutions, ll)


print solutions

