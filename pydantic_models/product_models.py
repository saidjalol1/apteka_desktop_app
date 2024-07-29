from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Optional, List
from datetime import date, datetime


class ProductIn(BaseModel):
    serial_number: Optional[Union[str, None]] = None
    name: Optional[Union[str, None]] = None
    
    box : Optional[Union[int, None]] = None
    amount_in_box : Optional[Union[int, None]] = None
    amount_in_package : Optional[Union[int, None]] = None
   
    produced_location : Optional[Union[str, None]] = None
    expiry_date : Optional[Union[str, None]] = None
    base_price : Optional[Union[float, None]] = None
    extra_price_in_percent : Optional[Union[int, None]] = None
    sale_price : Optional[Union[float, None]] = None
    sale_price_in_percent : Optional[Union[int, None]] = None
    discount_price : Optional[Union[float, None]] = None
    type_id :  Optional[Union[int, None]] = None
    score : Optional[Union[int, None]] = None
    overall_price : Optional[Union[float, None]] = None
    boxes_left : Optional[Union[int, None]] = None
    packages_left : Optional[Union[int, None]] = None
    units_left : Optional[Union[int, None]] = None

class CategoryIn(BaseModel):
    name : str

class CategoryOut(CategoryIn):
    id : int
    
    class Config:
        from_attributes = True
    
class ProductOut(ProductIn):
    id : int
    overall_amount : Optional[float] = None
    class Config:
        from_attributes = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
    

class QRData(BaseModel):
    data: str 
    

# @app.put("/product/edit")
# async def product_edit(product_id : int,product_update: product_models.ProductIn,current_user = current_user_dep,database = database_dep):
#     if current_user.is_admin:
#         product = database.query(models.Product).filter(models.Product.id == product_id).first()
#         if not product:
#             return {"error":"Mahsulot topilmadi"}

#         for key, value in product_update.model_dump(exclude_unset=True).items():
#             setattr(product, key, value)

#         database.commit()
#         database.refresh(product)
#         return product
#     else:
#         return {"error":"only admin can access this route"}
