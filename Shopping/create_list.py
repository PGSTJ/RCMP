import sqlite3 as sl
import os
import traceback

dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()


"""
Purpose: automatically create shopping list based on out of stock items 
         in kitchen inventory
	1. determines shopping days based on item availability
		 a) looks for priority items that necessitate shopping days 
        immediately
		priority:
			req for an upcoming chosen recipe
			user specified priority

To do:
	1. 
"""


def outStocks():
	"""Extracts out of stock items and category ID"""
	raw_data = [info for info in curs.execute('SELECT item, CID FROM KI_inventory WHERE stock_status=?', (False,))]
	categories = {info[0]:info[1] for info in curs.execute('SELECT * FROM KI_categories')}
	
	sorted_data = {}

	for item_name, cid in raw_data:
		id_name = categories[cid]

		if id_name not in sorted_data:
			sorted_data[id_name] = [item_name]
		elif sorted_data[id_name]:
			sorted_data[id_name].append(item_name)
		else:
			return False

	return sorted_data



if __name__ == '__main__':
	d = outStocks()
	print(d)



