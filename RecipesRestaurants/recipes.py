import sqlite3 as sl
import os
import traceback

dbf = 'database.db'
db_loc = os.path.abspath(dbf)
conn = sl.connect(db_loc, check_same_thread=False)
curs = conn.cursor()

RECIPE_UPLOAD = 'RecipesRestaurants\\recipe_list.txt'

def id_tracker(table:str, alphanum:str, swap:bool=False, number:tuple[int,bool]|bool=False) -> str:
    """
    Creates next ID int based on current table size. Allows a custom string combination
    of letters and numbers to "tag" the end of every ID.

    Optional Modifiers
        - swap - swaps the order of ID int and custom ID tag so ID tag is first and the ID int is second

            ```
            id_counter('test_table', 'TT', swap=True)
            ```

            Output:
            ```
            >>> 'TT1' instead of '1TT'
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


class RecipeCard():
    def __init__(self, name:str, id:int) -> None:
        self.id = id
        self.name = name
        self.preptime = 0
        self.cooktime = 0
        self.ingredients = ''
        self.instructions = ''
        self.tags = ''


def text_upload():
    """Upload names into recipe book and mark unfilled for later prompting"""
    try:
        with open(RECIPE_UPLOAD) as fn:
            grouped_by_line = [line.strip().split(',') for line in fn]


        all = [items for groups in grouped_by_line for items in groups]

        for items in all:
            id = id_tracker('all_recipes', 'R', swap=True)
            rc = RecipeCard(items, id)

            curs.execute('INSERT INTO all_recipes(id, name, prep_time, cook_time, ingredients, instructions, tags) VALUES (?,?,?,?,?,?,?)', (id, items, rc.preptime, rc.cooktime, rc.ingredients, rc.instructions, rc.tags))
        conn.commit()
        
        return True
    except Exception as e:
        traceback.print_exc()
        return False
    
def scan_incomplete_recipes() -> int | bool | None:
    """
    Scan recipe book for unfilled recipe information. 
    
    Returns: 
    - int amount of incomplete
    - bool for no incomplete
    - None for error
    
    """

    data = [info for info in curs.execute('SELECT id, name FROM all_recipes WHERE prep_time=?', (0,))]

    # extracted to inform user how many recipes are incomplete  
    amount = len(data)

    if amount == 0:
        return False
    elif amount > 0:
        return amount
    else:
        return None
    
"""
function for incomplete handling - coupled to html

subsequent message is to ask if user wants to fill now
if so will proceed to sequentially present unfilled recipes defined in data list
"""

if __name__ == '__main__':
    icr = scan_incomplete_recipes()

    if isinstance(icr, int):
        print(icr)
    elif isinstance(icr, bool):
        print('no incomplete recipes')
    elif isinstance(icr, None):
        print('error extracting data')
