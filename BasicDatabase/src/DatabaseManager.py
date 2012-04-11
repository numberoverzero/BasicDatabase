"""
Basic REPL DBM
"""

import Database

COMMANDS = [
    "GET",
    "SET",
    "UNSET",
    "BEGIN",
    "ROLLBACK",
    "COMMIT",
    "END"
    ]

def default_write_function(message):
    """Immediately prints output"""
    print message

class DatabaseManager(object):
    """
    A basic database manager 
    
     Supports interactive database querying and modification.
    """
    def __init__(self, database, prompt=None, write_function=None):
        self._database = database
        if prompt is not None:
            self._prompt = prompt
        else:
            self._prompt = ">>> "
        if write_function is None:
            self._writer = default_write_function
        else:
            self._writer = write_function

    def open_session(self):
        """Starts up an interactive session"""
        while True:
            inp_str = raw_input(self._prompt)
            inp_items = inp_str.split(" ")
            command, args = inp_items[0], inp_items[1:]
            command = command.upper()

            if command == "GET":
                name = args[0]
                value = self._database.get_item(name)
                if value is self._database.DefaultValue:
                    value = "NULL"
                self._writer(value)
            elif command == "SET":
                name = args[0]
                value = args[1]
                self._database.set_item(name, value)
            elif command == "UNSET":
                name = args[0]
                self._database.unset_item(name)
            elif command == "BEGIN":
                self._database.begin_transaction()
            elif command == "ROLLBACK":
                try:
                    self._database.rollback()
                except Database.InvalidRollbackException:
                    self._writer("INVALID ROLLBACK")
            elif command == "COMMIT":
                self._database.commit_transactions()
            elif command == "END":
                return
            else:
                self._writer("Unrecognized command [{}]".format(command))
