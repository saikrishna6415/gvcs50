import os
from cs50 import SQL
db = SQL("sqlite:///bak.db")

def main():
    f=open("menu.csv")
    reader = csv.reader(f)
    for items , flavors ,rate in reader:
         menu_list = db.execute("INSERT INTO menu_list (items , flavors ,rate) VALUES (:items , :flavors ,:rate)",{ "items": items , "flavors":flavors,"rate":rate})
    print(f"added menu_list from {items} of falvor {flavors}at the rate of {rate} ")
    db.commit()

if __name__ == "__main__":
    main()