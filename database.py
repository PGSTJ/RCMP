import sqlite3 as sl
import os

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

#################################################################################################
#####################    Kitchen Inventory    ###################################################
#################################################################################################


KI_CATEGORIES = [
    'produce',
    'dairy/eggs',
    'meat/poultry',
    'seafood',
    'frozen',
    'bread/bakery',
    'pantry',
    'sauces/spices',
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
    curs.execute('CREATE TABLE IF NOT EXISTS all_tags(id INT PRIMARY KEY, name VARCHAR(15))')

def reset_tag_list():
    """Clear tag list"""
    try:
        curs.execute('DROP TABLE all_tags')
        _create_all_tags()
        return True
    except:
        return False

if __name__ == '__main__':
    _create_recipe_book()
    _create_all_tags()

