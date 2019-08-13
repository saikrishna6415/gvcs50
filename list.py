import os

from cs50 import SQL

db = SQL("sqlite:///bak.db")

def main():
    menu_list = db.execute("SELECT * FROM menu_list")
    for menu in menu_list:
        print(f"Id_No. {menu['id']} {menu['items']} of flavor {menu['flavors']} at rate of {menu['rate']}.")


if __name__ == "__main__":
    main()