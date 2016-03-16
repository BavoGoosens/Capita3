

class LinkedList(object):

    def __init__(self, previous=None):
        self.previous = previous
        self.currentList = list()

    def couple(self):
        if self.previous is None:
            return list()
        else:
            coupled_list = self.previous.couple()
            coupled_list += self.currentList
            return coupled_list

    def add(self, entry):
        self.currentList.append(entry)