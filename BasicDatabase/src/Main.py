"""
Creates a database with an immediate writer
and opens a new session.
"""

import Database
import DatabaseManager

GENERIC_DB = Database.Database()
DBM = DatabaseManager.DatabaseManager(GENERIC_DB,'')
DBM.open_session()
