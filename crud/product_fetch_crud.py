from sqlalchemy.orm import Session
from database_models.models import Product
from pydantic_models.models import BaseProduct


# Returns Product According to The Id of it
def get_product(db : Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

#Returns Products with pagination
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

#Prduct Creation
def create(db: Session, product:BaseProduct):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
    