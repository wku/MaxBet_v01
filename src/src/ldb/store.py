from collections import defaultdict
from .transaction import TransactionBlock

class DataStore(object):

    def __init__(self):
        self._blocks = []
        self._variables = {}
        self._num_equal_to = defaultdict(int)

    def set(self, name, value, log=True):
        if name in self._variables:
            self.unset(name, log)

        if self.in_transaction() and log:
            self._blocks[-1].add_undo(self.unset, name, False)

        self._variables[name] = value
        self._num_equal_to[value] += 1

    def get(self, name):
        return self._variables.get(name, None)

    def unset(self, name, log=True):
        if name in self._variables:
            value = self._variables[name]

            if self.in_transaction() and log:
                self._blocks[-1].add_undo(self.set, name, value, False)

            del self._variables[name]
            self._num_equal_to[value] -= 1

    def numequalto(self, value):
        return self._num_equal_to[value]

    def begin(self):
        self._blocks.append(TransactionBlock())

    def rollback(self):
        if self.in_transaction():
            self._blocks.pop().rollback()

    def commit(self):
        self._blocks = []

    def in_transaction(self):
        return len(self._blocks) > 0
