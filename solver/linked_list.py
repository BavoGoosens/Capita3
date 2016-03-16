

class LinkedList(object):

    def __init__(self, previous=None):
        self.previous = previous
        self.currentList = list()

    def couple(self):
        if self.previous is None:
            return self.currentList
        else:
            return self.previous.couple().append(self.currentList)

    def add(self, entry):
        self.currentList.append(entry)