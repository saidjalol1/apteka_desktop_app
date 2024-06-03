from pydantic import BaseModel, Field, ConfigDict
from typing import Union


from datetime import date

class BaseProduct(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name : Union[str, None]
    price : Union[float, None]
    amount_in_package : Union[int, None]
    produced_location : Union[str, None]
    expiry_date : Union[date, None]
    score : Union[int, None]