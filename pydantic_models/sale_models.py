from typing import Union, Optional
from pydantic import BaseModel
from .product_models import ProductOut
from datetime import datetime
    
class Sell(BaseModel):
    check_id: int
    discount_card_id: Optional[Union[int, None]] = None
    from_discount_card: Optional[Union[float, None]] = None
    payment_type: str
    discount : Optional[Union[float, None]] = None
    person : Optional[Union[str, None]] = None
    total: float
    with_discount_card : bool = False
    

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
    amount : float
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
    

class DiscountCardIn(BaseModel):
    number : str
    amount : float
    name :str
    surname : str
    
class DiscountCardOut(DiscountCardIn):
    id : int
    qr_code_image : str
    

class TableData(BaseModel):
    headers: list[str]
    rows: list[list[str]]
    today: str