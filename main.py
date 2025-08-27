from database import Base, engine
from models import User, Category, Item

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(" Database and tables created.")
