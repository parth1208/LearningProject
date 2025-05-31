import json


class inventoryitem:
    def __init__(self, Item, qty, mfg, exp):
        self.Item = Item
        self.qty = qty
        self.mfg = mfg
        self.exp = exp

    def show(self):
        print(f"Item: {self.Item} | qty: {self.qty} | mfg: {self.mfg} | exp: {self.exp}")

    def to_inventory(self):
        return {"Item": self.Item, "qty": self.qty, "mfg": self.mfg, "exp": self.exp}

    @staticmethod
    def from_inventory(data):
        return inventoryitem(data["Item"], data["qty"], data["mfg"], data["exp"])


inventory = []  # list of dictionaries


def save_inventory():
    file_path = 'D:/Learning Project/File_Database/Inventory.json'
    data = [item.to_inventory() for item in inventory]
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        print("File not found.")


def load_inventory():
    global inventory
    file_path = 'D:/Learning Project/File_Database/Inventory.json'
    try:
        with open(file_path, "r") as f:
            inventory = [inventoryitem.from_inventory(items) for items in json.load(f)]
        return
    except FileNotFoundError:
        print("No saved Inventory Found.")
    except Exception as e:
        print(e)


def add_item():
    item = input("Enter item name:-")
    qty = int(input("Enter item qty:-"))
    mfg = input("Enter manufacturing date (YYYY-MM-DD):-")
    exp = input("Enter expiry date (YYYY-MM-DD):-")

    inventory.append(inventoryitem(item, qty, mfg, exp))
    save_inventory()


def view_inventory():
    if not inventory:
        print("Inventory is empty. \n")
        return
    for item in inventory:
        item.show()


def remove_item():
    global inventory
    item = ""
    item = input("Enter the item name:- ").strip().lower()
    if not item:
        print("Option: 0: Remove All Items  | 1: Specific item")
        command = int(input("Enter the Command:- "))
        if command == 1:
            remove_item()
        elif command == 0:
            inventory = []

        save_inventory()
        return

    for i, entry in enumerate(inventory):
        if entry["Item"] == item:
            del inventory[i]
            save_inventory()
            print("Item is Deleted.")
    return


def update_inventory():
    while True:
        print("Options: 1: Rename Item | 2: Update Qty | 3: Exit")  # | 3: Add Manufacturing Date | 4: Add Expiry Date
        Command = int(input("Enter the Command:"))
        match Command:
            case 1:  # Rename item.
                old_name = input("Enter the old name:-").strip().lower()
                new_name = input("Enter the new name:-").strip().lower()
                update = False
                for entry in inventory:
                    if entry["Item"] == old_name:
                        entry["Item"] = new_name
                        update = True

                if update:
                    print(f"Inventory item Renamed '{old_name}' to '{new_name}'.")
                else:
                    print(f"No item found with name '{old_name}'.")

            case 2:  # Update Qty
                item_name = input("Enter the item name:-").strip().lower()

                for entry in inventory:
                    if entry["Item"] == item_name:
                        print(f"Item is found with {entry["Qty"]} Qty.")
                        new_qty = int(input(f"Enter the new qty for '{item_name}' :-"))
                        entry["Qty"] = new_qty
                    else:
                        print("No Item found.")
                        return

            case 3:
                break

            case _:
                print("Invalid Command.")


def search_item():
    itemname = input("Enter the item name:-").strip().lower()
    for items in inventory:
        if items.Item.lower() == itemname:
            items.show()
            return
    print("No Item Found.")


def low_stock_item(threshold=5):
    found = False
    for items in inventory:
        if items.qty <= 5:
            items.show()
            found = True
    if not found:
        print("No Item qty is less then 5.")


def inventory_manager():
    load_inventory()
    while True:
        while True:
            try:
                print("Options: ( 1: Add | 2: View | 3: Update | 4: Remove | 5: Search | 6: Low Stock | 7: Exit )")
                Command = int(input("Enter the Command:-"))
                if Command in range(1, 8):
                    break
                else:
                    print("Please enter a number that are mention above options.")

            except ValueError:
                print("Please enter a number that are mention above options.")

        match Command:
            case 1:
                add_item()
            case 2:
                view_inventory()
            case 4:
                remove_item()
            case 3:
                update_inventory()
            case 5:
                search_item()
            case 6:
                low_stock_item()
            case 7:
                break
            case _:
                print("Invalid Command.\n")


inventory_manager()
