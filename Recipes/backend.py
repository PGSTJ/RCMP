import sqlite3 as sl
import os

dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()



class RecipeCard():
    def __init__(self) -> None:
        pass

