from typing import Union, Optional
from pydantic import BaseModel
from .product_models import ProductOut

    
class Sell(BaseModel):
    check_id: int
    cash : Optional[Union[float, None]] = None
    card : Optional[Union[float, None]] = None
    debt : Optional[Union[float, None]] = None
    discount : Optional[Union[float, None]] = None
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

class Return(BaseModel):
    product_id : int
    box : Optional[Union[int, None]] = None
    amount_in_box : Optional[Union[int, None]] = None
    amount_in_package : Optional[Union[int, None]] = None
    

class CheckLayout(BaseModel):
    name : str
    logo : str
    phone : str
    address : str
    image : str
    shift_id : int