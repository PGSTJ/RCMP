"""
Purpose: formats the meal planning csv files for meal planning related features
	1. divides meals into categories, separates desserts etc from dinner 
     randomization
	2. 

Tasks left:
	1. correlate meal randomization with in stock status in inventory
		a) requires recipes
"""

import random


# creates master dct of meal category lists
def readData(fileName="Meal Planner.csv"):
	file = open(fileName, "r")

	master_dct = {}

	for line in file:

		list_int = line.strip().split(",")

		if "" in list_int:
			idx = list_int.index("")
			categories_list = list_int[1:idx]
			master_dct[list_int[0]] = categories_list

		else:
			categories_list = list_int[1:]
			master_dct[list_int[0]] = categories_list

	file.close()

	return master_dct


# returns a list containing every meal
# input: master dictionary of meals
def allMeals(dictionary):
	all_meals = []

	for key in dictionary:
		if key != "Days" and key != "Baked" and key != "Sides":
			list_int = dictionary.get(key)

			for item in list_int:
				str_int = item

				all_meals.append(str_int)

	return all_meals


# returns random meal from master list
def randomizeMealPicker(list):
	choice = random.choice(list)

	print(choice)