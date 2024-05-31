from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from database_config.database_conf import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    amount_in_package = Column(Integer)
    ramainder = Column(Integer)
    produced_location = Column(String)
    expiry_date = Column(Date)
    score = Column(Integer)
    
    