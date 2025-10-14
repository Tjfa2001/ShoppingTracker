import sys
from unittest import case
import category_assigner as ca

def select_option():
    print("What would you like to do?")
    option = input("""1: Add a new item category\
                      \n2: Assign a category to an item\
                      \n3: Remove an item category\
                      \n4: View all categories\
                      \n5: Exit\
                      \nPlease enter the number of your choice: """)
    return option

def add_category():
    assigner = ca.CategoryAssigner("Sample Item")
    category = assigner.get_category()
    print(f"Assigned category: {category}")

if __name__ == "__main__":
    #option = select_option()
    option = '0'
    while option != '5':
        match option:
            case '1':
                assigner = ca.CategoryAssigner()
                assigner.category = input("Enter the new category name: ")
                assigner.add_category()
            case '2':
                assigner = ca.CategoryAssigner()
            case '3':
                assigner = ca.CategoryAssigner() 
                assigner.remove_category()
            case '4':
                assigner = ca.CategoryAssigner()
                assigner.view_categories()          
            case '5':
                print("Goodbye!")
            case _:
                print("Invalid option selected.")
        option = select_option()
        print(f"You selected option {option}")