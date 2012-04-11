"""
A basic Database, with get/set/unset,

uses Transactions, supporting rollback/commit
"""

import Commands

class InvalidRollbackException(Exception):
    """
    Thrown when a rollback is attempted on a database

    with no open transactional blocks.
    """
    
    def __init__(self, database):
        Exception.__init__(self)
        self.database = database
        
class Database(object):
    """
    A simple database, with a limited command set.

    Does not store to disk; all values are kept in memory.
    """
    def __init__(self):
        self._default_value = None
        self._table = dict()
        self._transactions = []
        self._current_transaction = None
        self._in_transaction = False

    def __g_current_transaction(self):
        """get_item the database's current transaction"""
        if len(self._transactions) > 0:
            return self._transactions[-1]
        return None
    CurrentTransaction = property(__g_current_transaction)

    def __g_default_value(self):
        """get_item the default value for null elements in the Database"""
        return self._default_value
    DefaultValue = property(__g_default_value)

    def set_item(self, name, value):
        """Set the value of name"""
        if not self._in_transaction:
            self._table[name] = value
        else:
            set_command = Commands.Set(name, value)
            self.CurrentTransaction.add_command(set_command)

    def unset_item(self, name):
        """Unset the value of name"""
        if not self._in_transaction:
            self._table.pop(name, None)
        else:
            unset_command = Commands.Unset(name, self._default_value)
            self.CurrentTransaction.add_command(unset_command)
            
    def get_item(self, name):
        """
        Gets the value of name
        
        Returns DefaultValue if name isn't found
        """
        if self._in_transaction:
            #Reverse iteration, since we want the most recent value
            for transaction in reversed(self._transactions):
                if transaction.is_modifying(name):
                    return transaction.get_item(name)
        return self._table.get(name, self._default_value)
            
    def begin_transaction(self):
        """Begin a new transaction"""
        self._transactions.append(Transaction())
        self._in_transaction = True

    def rollback(self):
        """
        Rollback the most recent transaction
        
        Raises InvalidRollbackException 
            when there is no transaction to rollback
        """
        if not self._in_transaction:
            raise InvalidRollbackException(self)
        else:
            self._transactions.pop()
            if self.CurrentTransaction is None:
                self._in_transaction = False

    def commit_transactions(self):
        """Commit all pending transactions to the database"""
        self._in_transaction = False
        for transaction in self._transactions:
            transaction.commit(self)
        self._transactions = []

class Transaction(object):
    """A group of commands that can be applied to a database"""

    def __init__(self):
        self._commands = []
        self._modifies = set()

    def add_command(self, command):
        """Add a new command to this transaction"""
        self._commands.append(command)
        self._modifies.add(command.name)
        
    def is_modifying(self, name):
        """True if any command modifies the varialiable [name]"""
        return name in self._modifies

    def get_item(self, name):
        """
        Get the most recent value of name
        
        Returns None if this transaction does not modify that name
        """
        if not self.is_modifying(name):
            return None
        #Reverse iteration, since we want the most recent value
        for command in reversed(self._commands):
            if not hasattr(command, 'name') or command.name != name:
                continue
            return command.value

    def commit(self, database):
        """Commit all pending commands to the database"""
        for command in self._commands:
            command.commit(database)
