import sqlite3 as sl
import json
import os
import traceback

"""
This file holds all database information

Intra-Database groupings:
    Kitchen Inventory (KI)
    Stores/Shopping (SS)
    Restaurants (Rs)
    Recipes (Rc)

Abbreviations:
    CID = Category (inventory) ID
    IID = Inventory ID
    SID = Store ID
    LID = Location ID
    AID = Address ID
    TID = Tag (recipes) ID
        TT - tag type

Pertinent order of creation:
    1. SS_locations
    2. SS_all_stores
    3. KI_inventory

    tags
    Rs_all_restaurants


User filled tables:
    address_book
    locations
    KI_inventory
    SS_all_stores
    SS_shopping_list
    Rs
"""

dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()


def _create_address_book():
    """Table holds all addresses for stores and restaurants"""
    curs.execute('CREATE TABLE IF NOT EXISTS address_book(id INT PRIMARY KEY, line VARCHAR(30), city VARCHAR(20), state VARCHAR(2), zip INT, grouping VARCHAR(2))')

def reset_address_book():
    """Clear address book"""
    try:    
        curs.execute('DROP TABLE address_book')
        _create_address_book()
        return True
    except:
        return False
    
"""
UTILITY TYPE FUNCTIONS - CONSIDERING A UTILITY CLASS PENDING AMOUNT OF FUNCTIONS
"""


def id_tracker(table:str, alphanum:str, swap:bool=False, number:tuple[int,bool]|bool=False) -> str:
    """
    Creates next ID int based on current table size. Allows a custom string combination
    of letters and numbers to "tag" the end of every ID.

    Optional Modifiers
        - swap - swaps the order of ID int and custom ID tag so ID tag is first and the ID int is second

            ```
            id_counter('test_table', 'TT', swap=True)
            ```
        - number - tuple formatter containing a set number to include in each ID as the first index and option
        to replace the numerical counting with the set number 

            ```
            id_counter('test_table', 'TT', number=(0, True))
            ```

    """
    # overrides counting and returns set number with custom tag qualifier
    if number and number[1]:
        count = str(number[0])
    else:
        stmt = f'SELECT id FROM {table}'
        all_items = [_ for _ in curs.execute(stmt)]

        if len(all_items) == 0:
            count = str(1)
        else:
            count = str(len(all_items) + 1)

    if swap:
        final_id = alphanum + count
    else:
        final_id = count + alphanum
        
    return final_id
        



#################################################################################################
#####################    Kitchen Inventory    ###################################################
#################################################################################################


KI_CATEGORIES = [
    'produce',
    'dairy_eggs',
    'meat_poultry',
    'seafood',
    'frozen',
    'bread_bakery',
    'pantry',
    'sauces_spices',
    'snacks',
    'beverages'
]


def _create_categories():
    """Creates DB table of kitchen inventory categories"""
    curs.execute('CREATE TABLE IF NOT EXISTS KI_categories(id VARCHAR(2) PRIMARY KEY, name VARCHAR(50))')

    for num, name in enumerate(KI_CATEGORIES):
        id = 'C' + str(num)

        curs.execute('INSERT INTO KI_categories(id, name) VALUES (?,?)', (id, name))
        conn.commit()

def reset_categories():
    """Clear category list"""
    try:    
        curs.execute('DROP TABLE KI_categories')
        _create_categories()
        return True
    except:
        return False

def _create_inventory():
    """Creates DB table of kitchen inventory; must have store and category tables created for FKs"""
    curs.execute('CREATE TABLE IF NOT EXISTS KI_inventory(id INT PRIMARY KEY, item VARCHAR(50), CID VARCHAR(2), SID VARCHAR(4), stock_status BOOL, FOREIGN KEY (CID) REFERENCES KI_categories(id), FOREIGN KEY (SID) REFERENCES SS_all_stores(id))')

def reset_inventory():
    """Clear inventory"""
    try:
        curs.execute('DROP TABLE KI_inventory')
        _create_inventory()
        return True
    except:
        return False


#################################################################################################
#####################    Stores/Shopping    #####################################################
#################################################################################################


def _create_store_list():
    """Create list of stores; must have existing address book for FK"""
    curs.execute('CREATE TABLE IF NOT EXISTS SS_all_stores(id VARCHAR(4) PRIMARY KEY, name VARCHAR(50), AID VARCHAR(4), FOREIGN KEY (AID) REFERENCES address_book(id))')

def reset_store_list():
    """Clear store list"""
    try:
        curs.execute('DROP TABLE SS_all_stores')

        _create_store_list()
        return True
    except:
        return False

def _create_shopping_list():
    """Creates table for shopping list; must have KI inventory and SS stores tables created for FKs"""
    curs.execute('CREATE TABLE IF NOT EXISTS SS_shopping_list(IID INT, SID VARCHAR(4), FOREIGN KEY (IID) REFERENCES KI_inventory(id), FOREIGN KEY (SID) REFERENCES SS_all_stores(id))')

def reset_shopping_list():
    """Recreates shopping list"""
    try:    
        curs.execute('DROP TABLE SS_shopping_list')
        _create_shopping_list()
        return True
    except:
        return False


#################################################################################################
#####################    Restaurants    #########################################################
#################################################################################################


def _create_restaurants_list():
    """Create table of all documented restaurants"""
    curs.execute('CREATE TABLE IF NOT EXISTS Rs_all_restaurants(id VARCHAR(5) PRIMARY KEY, name VARCHAR(50), AID VARCHAR(4), tags TEXT, FOREIGN KEY (AID) REFERENCES address_book(id))')

def reset_restaurant_list():
    """Resets restaurant list"""
    try:
        curs.execute('DROP TABLE Rs_all_restaurants')
        _create_restaurants_list()
        return True
    except:
        return False


#################################################################################################
#####################    Recipes    #############################################################
#################################################################################################

TAG_JSON_PATH = 'Recipes\\tags.json'

def _create_recipe_book():
    """
    Create table of all recipes

    Times are in minutes
    Ingredients are previously formatted list
    Tags are previously formatted list of FKs
    """
    curs.execute('CREATE TABLE IF NOT EXISTS all_recipes(id INT PRIMARY KEY, name VARCHAR(20), prep_time INT, cook_time INT, ingredients TEXT, instructions TEXT, tags TEXT)')

def reset_recipe_list():
    "Clears recipe book"
    try:
        curs.execute('DELETE TABLE all_recipes')
        _create_recipe_book()
        return True
    except:
        return False

def _create_all_tags():
    """Creates tables of all used tags"""
    curs.execute('CREATE TABLE IF NOT EXISTS all_tags(id INT PRIMARY KEY, name VARCHAR(15), type VARCHAR(20), type_id VARCHAR(7))')

    # import tags from json
    with open(TAG_JSON_PATH) as fn:
        tag_types = json.load(fn)

    
    try:
        type_id = 0
        for types in tag_types:
            for tags in tag_types[types]['options']:
                tid = id_tracker('all_tags', 'TID')
                tid_TT = id_tracker('all_tags', tag_types[types]['type abbreviation'], number=(type_id, True))

                curs.execute('INSERT INTO all_tags(id, name, type, type_id) VALUES (?,?,?,?)', (tid, tags, types, tid_TT))
                conn.commit()
            type_id += 1

        return True
    except Exception as e:
        traceback.print_exc()
        print('error recreating all_tags table')
        return False

def reset_tag_list():
    """Clear tag list"""
    try:
        curs.execute('DROP TABLE all_tags')
        if _create_all_tags():
            return True
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    if reset_tag_list():
        print('done')