from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from database_config.database_conf import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    serial_number = Column(String)
    name = Column(String)
    price = Column(Float)
    amount = Column(Integer)
    amount_in_package = Column(Integer)
    remainder = Column(Integer)
    produced_location = Column(String)
    expiry_date = Column(Date)
    score = Column(Integer)

    sale_product = relationship("SaleItem", back_populates="sale_product_items")


class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    amount_from_package = Column(Integer)
    total_sum = Column(Float)
    
    product_id = Column("Product", ForeignKey('products.id'))
    sale_id = Column("Sale", ForeignKey('sale.id'))
    
    sale_product_items = relationship("Product", back_populates="sale_product")
    sale = relationship("Sale", back_populates="items")
    

class Sale(Base):
    __tablename__ = "sale"
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    date_added = Column(Date)
    owner_id = Column("User", ForeignKey('users.id'))
    
    sale_owner = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale")



# User models 

class UserScores(Base):
    __tablename__ = "user_scores"
    
    id = Column(Integer, primary_key=True)
    score = Column(Float)
    date_scored = Column(Date)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("User", back_populates="scores")


class UserSalaries(Base):
    __tablename__ = "user_salaries"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    type = Column(String)
    date_received = Column(Date)
    giver_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    giver = relationship('User', foreign_keys=[giver_id], back_populates='salaries_given')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='salaries_received')


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    
    first_name = Column(String)
    last_name = Column(String)
    born_date = Column(Date)
    phone_number = Column(String)
    address = Column(String)
    shift = Column(Integer)
    
    scores = relationship("UserScores", back_populates="owner")
    salaries_received = relationship('UserSalaries', foreign_keys='UserSalaries.receiver_id', back_populates='receiver')
    salaries_given = relationship('UserSalaries', foreign_keys='UserSalaries.giver_id', back_populates='giver')
    sales = relationship("Sale", back_populates="sale_owner")