"""
The Command class for database actions

Includes basic commands set/unset
"""

class Command(object):
    """Any action that can be committed to a database."""
    name = None
    
    def __init__(self):
        pass

    def commit(self, database):
        """Commit the command to the database"""
        pass

    def _str(self):
        """Inheritable __str__ function"""
        return "generic_command"
    def __str__(self):
        return self._str()

class Set(Command):
    """
    Set a variable [name] to the value [value].

    Neither variable names nor values may contain spaces.
    """
    def __init__(self, name, value):
        Command.__init__(self)
        self.name = name
        self.value = value

    def commit(self, database):
        database.set_item(self.name, self.value)

    def _str(self):
        return "SET {name} {value}".format(name=self.name,
                                          value=self.value)
        
class Unset(Command):
    """Unset the variable [name]."""
    def __init__(self, name, value):
        Command.__init__(self)
        self.name = name
        self.value = value

    def commit(self, database):
        database.unset_item(self.name)
        
    def _str(self):
        return "UNSET {name}".format(name=self.name)
