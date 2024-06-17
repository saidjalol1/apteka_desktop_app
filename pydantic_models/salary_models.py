from datetime import date, datetime
from typing import Union, Optional
from pydantic import BaseModel



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
        
        

    
