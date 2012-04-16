"""
A basic Database, with get/set/unset,

uses Transactions, supporting rollback/commit
"""

class InvalidRollbackException(Exception):
    """
    Thrown when a rollback is attempted on a database

    with no open transactions.
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
        self._table = dict()
        self._transactions = []
        self._current_transaction = None
        self._in_transaction = False

    def __get_current_transaction(self):
        """get_item the database's current transaction"""
        if len(self._transactions) > 0:
            return self._transactions[-1]
        return None
    CurrentTransaction = property(__get_current_transaction)

    def __setitem__(self, name, value):
        """Set the value of name"""
        if not self._in_transaction:
            self._table[name] = value
        else:
            self.CurrentTransaction[name] = value

    def __getitem__(self, name):
        """
        Gets the value of name
        
        Returns None if name isn't found
        """
        if self._in_transaction:
            #Reverse iteration, since we want the most recent value
            for transaction in reversed(self._transactions):
                if transaction.is_modifying(name):
                    return transaction[name]
        return self._table.get(name, None)
    
    def __delitem__(self, name):
        """Remove name from the database"""
        if not self._in_transaction:
            self._table.pop(name, None)
        else:
            self.CurrentTransaction[name] = None
            
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
    """A group of changes that can be applied to a database"""

    def __init__(self):
        self._temp_table = dict()

    def is_modifying(self, name):
        """True if name is modified in this transaction"""
        return name in self._temp_table

    def __getitem__(self, name):
        """Get the most recent value of name"""
        return self._temp_table.get(name, None)
    
    def __setitem__(self, name, value):
        self._temp_table[name] = value

    def commit(self, database):
        """Commit all pending commands to the database"""
        for name, value in self._temp_table.iteritems():
            database[name] = value
