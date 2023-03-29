"""
Purpose: upload and formatting of kitchen inventories
	1. Stores what items in the inventory are in stock
	2. Data is stored in dictionary values, individualized to category:stock pairs
		a) Does not contain category titles within dictionary, but is meant to be used 
			 as an overall repository for other functions to refer to

Current Task
	1. 
"""


# categorize inventory
# returns list of lists of categories/boolean in status
def uploadInv(fileName="Inventory_P.csv"):

	file = open(fileName, "r")
	master_list = []

	for line in file:
			list_int = line.strip().split(",")

			# removes empty spaces within each category
			blank_check = True
			while blank_check is True:
					if "" in list_int:
							list_int.remove("")
					elif "" not in list_int:
							blank_check = False

			master_list.append(list_int)

	file.close()

	return master_list


# returns list of lists of only the categories
def extractCateg(master):
	categories = master
	for item in master:
		idx = categories.index(item)
		for item1 in item:
			if "In stock" in item1:
				before = categories[:idx]
				after = categories[idx + 1:]
				categories = before + after

	return categories


# returns a list of lists of only the boolean in stock status
def extractAvail(master):
	stocked = []

	for item in master:
			for item2 in item:
					if "In stock" in item2:
							stocked.append(item)

	return stocked


# correlate availability
# returns dictionary
def availability(master, stock):

	# zip both lists together in order to loop through simultaneously
	both_lists = zip(master, stock)
	master_dct = {}

	# simultaneous looping
	for item1, item2 in both_lists:
			duration = len(item1)

			int_zip = zip(item1, item2)

			# correlating product with boolean in stock status
			for itemA, itemB in int_zip:
					for num in range(1, duration, 1):
							master_dct[item1[num]] = item2[num]

	return master_dct


# creates dictionary of categories
# keys are category titles with values being the inventory as a list
def indivCateg(categories):
	categ_dct = {}

	for lists in categories:
			for items in lists:
					categ_dct[lists[0]] = lists[1:]

	return categ_dct