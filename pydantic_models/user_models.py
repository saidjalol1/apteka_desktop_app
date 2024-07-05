from datetime import date, datetime
from typing import Union, Optional
from pydantic import BaseModel
from .sale_models import SaleItemOut


class User(BaseModel):
    id: Union[int, None]
    username : Union[str, None]
    password : Union[str, None]
    is_admin : Union[bool, None]
   
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    username : Optional[str] = None
    hashed_password : Optional[str] = None
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


class UserExpancesIn(BaseModel):
    name : str
    amount : float

class UserExpancesOut(UserExpancesIn):
    id : Optional[Union[int, None]] = None

    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    username: str
    password: str

class ShiftIn(BaseModel):
    name : str
    
class UserShiftOut(ShiftIn):
    id : int
    
class UserScoreOut(BaseModel):
    score : float
    date_scored : datetime
    item : SaleItemOut
    
class UserOut(BaseModel):
    id : id
    first_name : str
    last_name : str
    
    class Config:
        from_attributes = True