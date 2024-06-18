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
    expiry_date : Optional[Union[date, None]] = None
    
    base_price : Optional[Union[float, None]] = None
    extra_price_in_percent : Optional[Union[int, None]] = None
    sale_price : Optional[Union[float, None]] = None
    sale_price_in_percent : Optional[Union[int, None]] = None
    discount_price : Optional[Union[float, None]] = None
   
    score : Optional[Union[int, None]] = None
    

    class Config:
        from_attributes = True
    
    
class ProductOut(ProductIn):
    id : int

    class Config:
        from_attributes = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
    