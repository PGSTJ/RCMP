import os
import sqlite3 as sl
import traceback
from database import _next_id


dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()


INVENTORY_PATH = 'Kitchen_Inventory\\inventory.csv'


def formatInvCSV():
	"""Formats inventory file to dictinoary of lists of items for database upload"""

	with open(INVENTORY_PATH) as fn:
		# extracts category names into unformatted string
		# categories list should be identical to constant in database.py
		categories_unf = fn.readline().strip().lower()
		categories = categories_unf.split(',') 
		cat_dict = {name:[] for name in categories}

		# similar to category titles, format strings into list, then iterate and make into classes
		# every intra-list should have length 10 - regardless of empty spaces
		master_list_unf = [line.strip().split(',') for line in fn]

	for lists in master_list_unf:
		for items in lists:
			if len(items) != 0:
				idx = lists.index(items)
				cat_name = categories[idx]
				cat_dict[cat_name].append(items)

	return cat_dict
				

def upload_to_db(master_dict:dict) -> bool:
	"""Upload to KI_Inventory Table after pulling respsective CID from KI_categories"""

	try:
		for categories in master_dict:
			cid = [_ for _ in curs.execute('SELECT id FROM KI_categories WHERE name=?', (categories,))][0][0]
			
			

			for items in master_dict[categories]:
				if not _item_exists(items):
					id = _next_id('KI_inventory')  # FIXME: Unable to upload inventory because cannot assign ID - not finding module with helper function
					# TODO: Include SID once shopping functionality worked
					curs.execute('INSERT INTO KI_inventory(id, item, CID, SID, stock_status) VALUES (?,?,?,?,?)', (id, items, cid, 0, True)) 
					conn.commit()	
		return True
	except Exception as e:
		print(traceback.print_exc(e))
		return False

def _item_exists(item:str) -> bool:
	"""helper function for DB inv upload - checks if item exists in table"""
	all_items = [_ for _ in curs.execute('SELECT id FROM KI_inventory WHERE item=?', (item,))]
	if all_items:
		return True
	else:
		return False



def extract_inventory() -> dict:
	"""Pulls inventory from database into dict for HTML display"""
	
	# create dictionary to relate id to category name
	category_info = {id:name for id,name in curs.execute('SELECT id, name FROM KI_categories')}
	# this dictionary will be returned with inventory values with respsective category keys
	all_data = {category_info[data]:[] for data in category_info}

	# pull inventory from database and format into above dictionary
	item_info = [data for data in curs.execute('SELECT item, CID FROM KI_inventory')]
	for item,cid in item_info:
		cat_name = category_info[cid]
		all_data[cat_name].append(item)
		

	return all_data


if __name__ == '__main__':
	if upload_to_db():
		print('inv uploaded')
