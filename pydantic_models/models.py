from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Optional

from datetime import date

class BaseProduct(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name : Union[str, None]
    price : Union[float, None]
    amount_in_package : Union[int, None]
    produced_location : Union[str, None]
    expiry_date : Union[date, None]
    score : Union[int, None]
    
class User(BaseModel):
    id: Union[int, None]
    username : Union[str, None]
    password : Union[str, None]
    is_admin : Union[bool, None]

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
        
class Token(BaseModel):
    access_token: str
    token_type: str
    