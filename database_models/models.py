from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship

from database_config.database_conf import Base, current_time


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    products = relationship("Product", back_populates="type")
    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    
    serial_number = Column(String)
    name = Column(String)
    
    
    box = Column(Integer)
    amount_in_box = Column(Integer)
    amount_in_package = Column(Integer)
    
    produced_location = Column(String)
    expiry_date = Column(Date)
    
    base_price = Column(Float)
    extra_price_in_percent = Column(Integer)
    sale_price = Column(Float)
    sale_price_in_percent = Column(Float)
    discount_price = Column(Float)
    overall_amount = Column(Integer, default=0)
    type_id  = Column("Category", ForeignKey('category.id'))
    score = Column(Integer)
    sale_product = relationship("SaleItem", back_populates="sale_product_items")
    type = relationship("Category", back_populates="products")


class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True)
    amount_of_box = Column(Integer)
    amount_of_package = Column(Integer)
    amount_from_package = Column(Integer)
    total_sum = Column(Float)
    product_id = Column("Product", ForeignKey('products.id'))
    sale_id = Column("Sale", ForeignKey('sale.id'))
    
    sale_product_items = relationship("Product", back_populates="sale_product")
    sale = relationship("Sale", back_populates="items")
    user_scores = relationship("UserScores", back_populates="item")


class Sale(Base):
    __tablename__ = "sale"
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    date_added = Column(DateTime, default=current_time)
    status = Column(String)
    person = Column(String)
    discount = Column(Float)
    cash = Column(Float)
    debt = Column(Float)
    card = Column(Float)
    owner_id = Column("User", ForeignKey('users.id'))
    
    sale_owner = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale")


# User models 
class UserScores(Base):
    __tablename__ = "user_scores"
    
    id = Column(Integer, primary_key=True)
    score = Column(Float)
    date_scored = Column(DateTime, default=current_time)
    owner_id = Column(Integer, ForeignKey('users.id'))
    sale_item_id = Column(Integer, ForeignKey("sale_items.id"))
    
    item = relationship("SaleItem", back_populates="user_scores")
    owner = relationship("User", back_populates="scores")


class UserSalaries(Base):
    __tablename__ = "user_salaries"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    type = Column(String)
    date_received = Column(DateTime, default=current_time)
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
    
    scores = relationship("UserScores", back_populates="owner")
    shift_id = Column(Integer, ForeignKey('users_shift.id'))
    shift = relationship("UserShift", back_populates="users")
    salaries_received = relationship('UserSalaries', foreign_keys='UserSalaries.receiver_id', back_populates='receiver')
    salaries_given = relationship('UserSalaries', foreign_keys='UserSalaries.giver_id', back_populates='giver')
    sales = relationship("Sale", back_populates="sale_owner")
    
    expances = relationship("UserExpances", back_populates="expance_owner")


class UserShift(Base):
    __tablename__ = "users_shift"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    users = relationship("User", back_populates="shift")
    check_layout = relationship("CheckLayout", back_populates="check_shift")


class CheckLayout(Base):
    __tablename__ = "check_layout"
     
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    image  = Column(String)
    logo = Column(String)
    phone = Column(String)
    address = Column(String)
    shift_id = Column(Integer, ForeignKey('users_shift.id'))
    
    
    check_shift = relationship("UserShift", back_populates="check_layout")
    

class UserExpances(Base):
    __tablename__ = "user_expances"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    date_added = Column(DateTime, default=current_time)
    
    expance_owner_id = Column(Integer, ForeignKey('users.id'))
    expance_owner = relationship("User", back_populates="expances")
    
    
class DiscountCard(Base):
    __tablename__ = "discount_cards"
    
    id = Column(Integer, primary_key=True)
    number = Column(String)
    amount = Column(Float)
    
    