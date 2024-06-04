from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from database_config.database_conf import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    amount_in_package = Column(Integer)
    remainder = Column(Integer)
    produced_location = Column(String)
    expiry_date = Column(Date)
    score = Column(Integer)
    

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
    date_received = Column(Date)
    receiver_id = Column(Integer, ForeignKey("users.id"))

    receiver = relationship("User", back_populates="salaries")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    
    first_name = Column(String)
    last_name = Column(String)
    born_date = Column(Date)
    phone_number = Column(String)
    address = Column(String)
    shift = Column(Integer)
    
    scores = relationship("UserScores", back_populates="owner")
    salaries = relationship("UserSalaries", back_populates="receiver")