# database.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# Base class for ORM
Base = declarative_base()

# -------------------------
# Models
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)  # <-- Added phone column

    items = relationship("Item", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, phone={self.phone})>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    items = relationship("Item", back_populates="category")

    def __repr__(self):
        return f"<Category(name={self.name})>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="lost")  # lost or found
    date_reported = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="items")
    category = relationship("Category", back_populates="items")

    def __repr__(self):
        return f"<Item(name={self.name}, status={self.status})>"


# -------------------------
# Database setup
# -------------------------
engine = create_engine("sqlite:///lost_and_found.db")
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)
