from sqlalchemy.orm import Session
from database_models.models import Product
from pydantic_models.product_models import ProductIn


# Returns Product According to The Id of it
def get_product(db, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

#Returns Products with pagination
def get_products(db):
    return db.query(Product).filter(Product.overall_amount > 0).all()

#Prduct Creation
def create(db, product:ProductIn):
    try:
        db_product = Product(**product.model_dump())
        db_product.overall_amount = db_product.amount_in_box * db_product.amount_in_package * db_product.box
        db_product.boxes_left = (db_product.overall_amount - (db_product.overall_amount % (db_product.amount_in_box * db_product.amount_in_package))) // (db_product.amount_in_box * db_product.amount_in_package)
        db_product.packages_left = (db_product.overall_amount % (db_product.amount_in_box * db_product.amount_in_package)) // db_product.amount_in_package
        db_product.units_left = (db_product.overall_amount % (db_product.amount_in_box * db_product.amount_in_package)) % db_product.amount_in_package
        db.add(db_product)
        db.commit()
        return {"success":"success"}
    except Exception as e:
        print(e)
        return {"message":e} 
    
    