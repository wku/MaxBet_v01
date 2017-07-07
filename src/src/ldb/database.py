import sys
from .store import DataStore

class Database(object):


    COMMANDS = ['SET', 'GET', 'UNSET', 'NUMEQUALTO', 'BEGIN', 'ROLLBACK', 'COMMIT', 'END']

    def __init__(self):
        self._store = DataStore()

    def execute(self, raw_cmd):

        tokens = raw_cmd.strip().split()

        cmd = tokens[0]
        args = tokens[1:]

        if cmd.upper() not in Database.COMMANDS:
            raise LookupError("The inputted command is not supported.")

        cmd_method = getattr(self, cmd.lower())

        method_arg_count = cmd_method.__code__.co_argcount - 1

        if len(args) != method_arg_count:
            raise TypeError("Wrong number of arguments for the command %s." % cmd)

        return cmd_method(*args)

    def set(self, name, value):
        self._store.set(name, value)

    def get(self, name):
        value = self._store.get(name)
        return value if value else "NULL"

    def unset(self, name):
        self._store.unset(name)

    def numequalto(self, value):
        return self._store.numequalto(value)

    def begin(self):
        self._store.begin()

    def rollback(self):
        if not self._store.in_transaction():
            return "NO TRANSACTION"

        self._store.rollback()

    def commit(self):
        if not self._store.in_transaction():
            return "NO TRANSACTION"

        self._store.commit()

    def end(self):
        sys.exit()


if __name__ == '__main__':
    db = Database()

    # for line in sys.stdin:
    #
    #     # line.strip() to check if user pressed enter with no input
    #     if line is not None and line.strip():
    #         try:
    #             result = db.execute(line)
    #             if result is not None:
    #                 print(result)
    #         except Exception as e:
    #             # Print the error message
    #             print(e)

    db.set('ee',11)
    print (db.get('ee'))