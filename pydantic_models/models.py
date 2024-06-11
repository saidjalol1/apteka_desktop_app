from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Optional, List

from datetime import date, datetime

class ProductIn(BaseModel):
    serial_number: Optional[Union[str, None]] = None
    name: Optional[Union[str, None]] = None
    price : Optional[Union[float, None]] = None
    amount : Optional[Union[int, None]] = None
    amount_in_package : Optional[Union[int, None]] = None
    produced_location : Optional[Union[str, None]] = None
    expiry_date : Optional[Union[date, None]] = None
    score : Optional[Union[int, None]] = None

    class Config:
        from_attributes = True
    
class ProductOut(ProductIn):
    id : int

    class Config:
        from_attributes = True
        
# User Models   
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
    shift : Optional[int] = None
    
    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    first_name: Optional[Union[str, None]] = None
    last_name: Optional[Union[str, None]] = None
    born_date: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        from_attributes = True



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
    amount : Optional[Union[int, None]] = None
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
    status : bool
    
    class Config:
        from_attributes = True
    
class UserScoreOut(BaseModel):
    score : float
    date_scored : datetime
    item : SaleItemOut