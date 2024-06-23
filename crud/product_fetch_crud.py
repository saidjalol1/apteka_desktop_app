from sqlalchemy.orm import Session
from database_models.models import Product
from pydantic_models.product_models import ProductIn


# Returns Product According to The Id of it
def get_product(db : Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

#Returns Products with pagination
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).filter(Product.overall_amount > 0).offset(skip).limit(limit).all()

#Prduct Creation
def create(db: Session, product:ProductIn):
    db_product = Product(**product.model_dump())
    if db_product.box is None or db_product.amount_in_box is None or db_product.amount_in_package is None:
        db_product.overall_amount = db_product.amount_in_box * db_product.amount_in_package * db_product.box
    else:
        return {"error":"Unprocessable entity"}
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"success":"success"}
    