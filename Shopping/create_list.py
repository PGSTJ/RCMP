"""
Purpose: automatically create shopping list based on out of stock items 
         in kitchen inventory
	1. determines shopping days based on item availability
		 a) looks for priority items that necessitate shopping days 
        immediately

To do:
	1. 
"""

# determine only what's out of stock
# input: dictionary of item-availability determination
# returns list of out of stock items
def outStocks(inventory):
	shop_list = []
	
	for key in inventory:
		if inventory[key] == "FALSE":
			shop_list.append(key)

	return shop_list
