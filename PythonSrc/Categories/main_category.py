import sys
#from unittest import case
import category_assigner as ca
import pyodbc as pdbc
import config
import os
import json

# Main method that loops through options that you can choose when this module is run
def run():
    option = '0'
    while option != '6':
        match option:
            case '1':
                assigner = ca.CategoryAssigner()
                assigner.category = input("Enter the new category name: ")
                assigner.add_category()
            case '2':
                assigner = ca.CategoryAssigner()
                assigner.assign_category_to_item()
            case '3':
                assigner = ca.CategoryAssigner() 
                assigner.remove_category()
            case '4':
                assigner = ca.CategoryAssigner()
                assigner.view_categories()  
            case '5':
                 # Might be useful to put the database connector class in the same directory level 
                 DictionaryLocation = os.path.abspath(os.path.join(os.path.dirname(__file__),"CategoryDict.json"))
                 with open(DictionaryLocation,'r') as CategoryDict:
                    dictionary = json.load(CategoryDict) 
                    for item in dictionary:
                        print("Updating Database...")
                        print(f"{item} -> {dictionary[item]}")
                        update_database(item_name = item, category=dictionary[item])
            case '6':
                print("Goodbye!")
            case '0':
                pass
            case _:
                print("Invalid option selected.")
        option = select_option()
        if option != 0:
            print(f"You selected option {option}")

def select_option():
    print("What would you like to do?")
    option = input("""1: Add a new item category\
                      \n2: Assign a category to an item\
                      \n3: Remove an item category\
                      \n4: View all categories\
                      \n5: Update database\
                      \n6: Exit\
                      \nPlease enter the number of your choice: """)
    return option

# Updates the database with a category for a given item
def update_database(item_name,category):
    
    connection = pdbc.connect(config.databaseConnectionString)
    connection.setencoding(encoding='utf-8')
    connection.setdecoding(pdbc.SQL_CHAR,encoding='utf-8')
    connection.setdecoding(pdbc.SQL_WCHAR,encoding='utf-8')
    cur = connection.cursor()
    
    try:
        cur.execute('CALL lidl.update_category(?,?);',(item_name,category))
    except pdbc.DatabaseError as err:
        cur.rollback()
        print(err.args[1])
    finally:
        cur.commit()

# Adds a category to the list of possible categories
def add_category():
    assigner = ca.CategoryAssigner("Sample Item")
    category = assigner.get_category()
    print(f"Assigned category: {category}")

if __name__ == "__main__":
    run()