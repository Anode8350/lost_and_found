from database import Session, User, Category, Item
import csv

STATUS = ("Lost", "Found", "Resolved")

def add_user():
    session = Session()
    try:
        name = input("Enter user name: ").strip()
        email = input("Enter user email: ").strip()
        phone = input("Enter user phone: ").strip()
        u = User(name=name, email=email, phone=phone)
        session.add(u)
        session.commit()
        print(" User added successfully.")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def add_category():
    session = Session()
    try:
        name = input("Enter category name: ").strip()
        desc = input("Enter category description: ").strip()
        c = Category(name=name, description=desc)
        session.add(c)
        session.commit()
        print(" Category added successfully.")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def report_item():
    session = Session()
    try:
        name = input("Enter item name: ").strip()
        desc = input("Enter item description: ").strip()

        print("Choose status:")
        for i, s in enumerate(STATUS, start=1):
            print(f"{i}. {s}")
        choice = int(input("Enter choice number: ").strip())
        status = STATUS[choice - 1]

        categories = session.query(Category).all()
        if not categories:
            print(" Please add a category first.")
            return
        for c in categories:
            print(f"{c.id}. {c.name}")
        cid = int(input("Enter category id: ").strip())

        users = session.query(User).all()
        if not users:
            print(" Please add a user first.")
            return
        for u in users:
            print(f"{u.id}. {u.name}")
        uid = int(input("Enter user id: ").strip())

        it = Item(name=name, description=desc, status=status, category_id=cid, user_id=uid)
        session.add(it)
        session.commit()
        print(" Item reported successfully.")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def list_items():
    session = Session()
    try:
        items = session.query(Item).join(User).join(Category).all()
        if not items:
            print("No items found.")
            return
        for it in items:
            print(f"[{it.id}] {it.name} - {it.status} | {it.category.name} | reporter: {it.user.name}")
    finally:
        session.close()

def search_items():
    session = Session()
    try:
        keyword = input("Enter keyword to search: ").strip()
        q = session.query(Item).join(User).join(Category).filter(
            (Item.name.ilike(f"%{keyword}%")) |
            (Item.description.ilike(f"%{keyword}%"))
        )
        items = q.all()
        if not items:
            print("No matching items found.")
            return
        for it in items:
            print(f"[{it.id}] {it.name} - {it.status} | {it.category.name} | reporter: {it.user.name}")
    finally:
        session.close()

def mark_resolved():
    session = Session()
    try:
        items = session.query(Item).filter(Item.status.in_(["Lost", "Found"])).all()
        if not items:
            print("No active items to resolve.")
            return
        for it in items:
            print(f"[{it.id}] {it.name} - {it.status}")
        iid = input("Enter item id to mark resolved: ").strip()
        item = session.get(Item, int(iid))
        if not item:
            print(" Item not found.")
            return
        item.status = "Resolved"
        session.commit()
        print(f" Item {item.name} marked as Resolved.")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def export_items_csv():
    session = Session()
    try:
        items = session.query(Item).join(User).join(Category).all()
        if not items:
            print("No items to export.")
            return
        with open("items_export.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Status", "Category", "Reporter"])
            for it in items:
                writer.writerow([it.id, it.name, it.status, it.category.name, it.user.name])
        print(" Items exported to items_export.csv")
    finally:
        session.close()

MENU = {
    "1": "Add user",
    "2": "Add category",
    "3": "Report item",
    "4": "List items",
    "5": "Search items",
    "6": "Mark item as Resolved",
    "7": "Export items to CSV",
    "8": "Exit",
}

def main():
    while True:
        print("\nLost & Found Menu:")
        for k, v in MENU.items():
            print(f"{k}. {v}")
        choice = input("Choose option: ").strip()
        if choice == "1": add_user()
        elif choice == "2": add_category()
        elif choice == "3": report_item()
        elif choice == "4": list_items()
        elif choice == "5": search_items()
        elif choice == "6": mark_resolved()
        elif choice == "7": export_items_csv()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
