class TransactionBlock(object):


    def __init__(self):
        self._undo_actions = []

    def add_undo(self, command, *args):
        self._undo_actions.append(UndoAction(command, args))

    def rollback(self):
        """Run all the undo actions."""
        for action in reversed(self._undo_actions):
            action.run()

        self._undo_actions = []


class UndoAction(object):

    def __init__(self, command, args):
        self._command = command
        self._args = args

    def run(self):
        self._command(*self._args)
