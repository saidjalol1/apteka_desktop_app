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
    discount : Optional[Union[int, None]] = None
    discount_price : Optional[Union[float, None]] = None
   
    score : Optional[Union[int, None]] = None
    
    retail_marks : Optional[Union[float, None]] = None
    retail_sum : Optional[Union[float, None]] = None
    nds : Optional[Union[float, None]] = None
    nds_price : Optional[Union[float, None]] = None


    class Config:
        from_attributes = True
    
class ProductOut(ProductIn):
    id : int

    class Config:
        from_attributes = True
        
# User Models 
class ShiftIn(BaseModel):
    name : str
    
class UserShiftOut(ShiftIn):
    id : int
    
class User(BaseModel):
    id: Union[int, None]
    username : Union[str, None]
    password : Union[str, None]
    is_admin : Union[bool, None]
   
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    username : Optional[str] = None
    password : Optional[str] = None
    is_admin : Optional[bool] = None
    
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    born_date : Optional[date] = None
    phone_number : Optional[str] = None
    address : Optional[str] = None
    shift_id : Optional[int] = None
    
    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    first_name: Optional[Union[str, None]] = None
    last_name: Optional[Union[str, None]] = None
    born_date: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    shift_id : Optional[int] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Salary mdels
class SalaryInModel(BaseModel):
    amount : Union[float, int]
    type : Union[str, None]
    date_received : Union[date, None]
    receiver_id : Union[int, None]
    
    class Config:
        from_attributes = True

        
class SalaryOutModel(SalaryInModel):
    id : int
    
    class Config:
        from_attributes = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

#Sale Models
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
    
    
class UserScoreOut(BaseModel):
    score : float
    date_scored : datetime
    item : SaleItemOut
    

class Sell(BaseModel):
    check_id: int
    payment_type: str
    total: float