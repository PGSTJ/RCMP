import sqlite3 as sl
import os


"""
Purpose: formats the meal planning csv files for meal planning related features
	1. Randomly chooses meal(s)
	2. Ensures in stock ingredients per recipe for chosen recipes
	3. Marks used recipes

Tasks left:

"""



dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()


import random

def randomizeMealPicker(list):
	"""Returns random meal (choice) from specified list"""
	choice = random.choice(list)

	return choice


def eligible_meals() -> list:
	"""Creates list of eligible meals - should have required ingredients in stock + open availablility per DB"""

	all_recipes = [item for item in curs.execute('SELECT id, name, ingredients FROM all_recipes WHERE available=?', (True,))]
	return all_recipes



if __name__ == '__main__':
	d = eligible_meals()
	print(d)