"""
Creates a database with an immediate writer
and opens a new session.
"""

import Database
import DatabaseManager

lines = []
def deferred_writer(line):
    lines.append(line)
def print_writer():
    print '\n'.join(lines)


GENERIC_DB = Database.Database()
DBM = DatabaseManager.DatabaseManager(GENERIC_DB, '', deferred_writer)
DBM.open_session()
print_writer()