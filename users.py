import os
from cs50 import SQL

db = SQL("sqlite:///bak.db")

def main():
    #menu list
    menu_list = db.execute("SELECT id,items, flavors,  rate FROM menu_list").fetchall()
    for menu in menu_list:
        print(f"menu {menu.items} is of flavour {menu.flavors} at the rate of {menu.rate}Rupees.")

    #promt user to select an menu
    menu_id = int(input("\n Menu ID:"))
    menu = db.execute("SELECT id, items, flavors,  rate FROM menu_list WHERE id = id ", { "id" : menu_id }).fetchone()

    #make sure menu is valid
    if menu_list is None:
        print(f"Error: No such item present.")
    return

    #user list
    users = db.execute("SELECT name  FROM users WHERE menu_id = :menu_id", {"menu_id":menu_id}).fetchall()


    print("\nUsers:")
    for user in users:
         print(user.name)
    if len(user)==0:
         print("No user Found")