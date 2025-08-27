from database import Base, engine
from models import User, Category, Item
from cli import run

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    run()
