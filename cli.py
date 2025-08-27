from database import Session
from models import User, Category, Item

STATUS = ("Lost", "Found")  
MENU = {                     
    "1": "Add user",
    "2": "Add category",
    "3": "Report item",
    "4": "List items",
    "5": "Exit",
}

def add_user():
    session = Session()
    try:
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone (optional): ").strip() or None
        user = User(name=name, email=email, phone=phone)
        session.add(user)
        session.commit()
        print(f" User added: {user.name}")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def add_category():
    session = Session()
    try:
        name = input("Category name: ").strip()
        desc = input("Description (optional): ").strip() or None
        cat = Category(name=name, description=desc)
        session.add(cat)
        session.commit()
        print(f" Category added: {cat.name}")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def _choose_user(session):
    users = session.query(User).order_by(User.name).all()  # list ✅ requirement
    if not users:
        print("No users found. Add a user first.")
        return None
    for u in users:
        print(f"- {u.id}: {u.name} ({u.email})")
    uid = input("Select user id: ").strip()
    return session.get(User, int(uid))

def _choose_category(session):
    cats = session.query(Category).order_by(Category.name).all()
    if not cats:
        print("No categories found. Add a category first.")
        return None
    for c in cats:
        print(f"- {c.id}: {c.name}")
    cid = input("Select category id: ").strip()
    return session.get(Category, int(cid))

def report_item():
    session = Session()
    try:
        name = input("Item name: ").strip()
        description = input("Description: ").strip()
        print("Status: 1) Lost  2) Found")
        s = input("Choose 1 or 2: ").strip()
        status = STATUS[0] if s == "1" else STATUS[1]

        user = _choose_user(session)
        if not user: return
        category = _choose_category(session)
        if not category: return

        item = Item(name=name, description=description, status=status,
                    user=user, category=category)
        session.add(item)
        session.commit()
        print(f" Item reported: {item.name} [{item.status}]")
    except Exception as e:
        session.rollback()
        print(f" Error: {e}")
    finally:
        session.close()

def list_items():
    session = Session()
    try:
        filt = input("Filter by (a)ll, (l)ost, (f)ound? ").lower().strip()
        q = session.query(Item).join(User).join(Category)
        if filt == "l":
            q = q.filter(Item.status == "Lost")
        elif filt == "f":
            q = q.filter(Item.status == "Found")
        items = q.order_by(Item.id.desc()).all()
        if not items:
            print("No items found.")
            return
        for it in items:
            print(f"[{it.id}] {it.name} - {it.status} | {it.category.name} | reporter: {it.user.name}")
    finally:
        session.close()

def run():
    print("\n=== Lost & Found Tracker ===")
    while True:
        for k, v in MENU.items():
            print(f"{k}. {v}")
        choice = input("Choose an option: ").strip()
        if choice == "1": add_user()
        elif choice == "2": add_category()
        elif choice == "3": report_item()
        elif choice == "4": list_items()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
