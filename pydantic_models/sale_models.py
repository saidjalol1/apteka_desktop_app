from typing import Union, Optional
from pydantic import BaseModel
from .product_models import ProductOut

    
class Sell(BaseModel):
    check_id: int
    payment_type: Optional[Union[str, None]] = None
    discount : Optional[Union[float, None]] = None
    person : Optional[Union[str, None]] = None
    total: float
    

class SaleItemIn(BaseModel):
    amount_of_box : Optional[Union[int, None]] = None
    amount_of_package : Optional[Union[int, None]] = None
    amount_from_package : Optional[Union[int, None]] = None
    total_sum : Optional[Union[float, None]] = None
    product_id : Optional[Union[int, None]] = None
    sale_id : int
    
    class Config:
        from_attributes = True


class SaleItemOut(SaleItemIn):
    id: int
    sale_product_items : ProductOut

    class Config:
        from_attributes = True


class CheckOut(BaseModel):
    id: int
    amount : int
    status : str

    class Config:
        from_attributes = True

class ReturnIn(BaseModel):
    amount_of_box : Optional[Union[int, None]] = None
    amount_of_package : Optional[Union[int, None]] = None
    amount_from_package : Optional[Union[int, None]] = None
    total_sum : Optional[Union[float, None]] = None
    product_id : Optional[Union[int, None]] = None
    return_id : int
    
class ReturnOut(ReturnIn):
    id: int
    returned_items : ProductOut

    class Config:
        from_attributes = True
        
class ResponceReturn(BaseModel):
    id: int
    discount : Optional[Union[float, None]] = None
    amount: float

    class Config:
        from_attributes = True
    
class CheckLayout(BaseModel):
    name : str
    logo : Optional[bytes]
    phone : str
    address : str
    image : str
    shift_id : int
    

class DiscountCardIn:
    number : Optional[Union[int, None]] = None
    amount : Optional[Union[int, None]] = None