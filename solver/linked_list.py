

class LinkedList(object):

    def __init__(self, previous=None):
        self.previous = previous
        self.currentList = list()

    def couple(self):
        if self.previous is None:
            return self.currentList
        else:
            coupled_list = self.previous.couple()
            return coupled_list.append(self.currentList)

    def add(self, entry):
        self.currentList.append(entry)