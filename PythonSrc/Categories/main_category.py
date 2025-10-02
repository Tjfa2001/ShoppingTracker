import sys
import category_assigner as ca

def select_option():
    print("What would you like to do?")
    option = input("""1: Add a new item category\
                      \n2: Assign a category to an item\
                      \n3: Remove an item category\
                      \n4: Exit\
                      \nPlease enter the number of your choice: """)
    return option

def add_category():
    assigner = ca.CategoryAssigner("Sample Item")
    category = assigner.get_category()
    print(f"Assigned category: {category}")

if __name__ == "__main__":
    option = select_option()
    print(f"You selected option {option}")
    if option == '1':
        add_category()