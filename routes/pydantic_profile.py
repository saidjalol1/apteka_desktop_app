from pydantic import BaseModel
from typing import Optional, Union, List
from pydantic_models.models import CreateUser

class UserScores(BaseModel):
    id : int
    score : Optional[float] = None

    class Config:
        from_attributes = True


class Profile(BaseModel):
    user : CreateUser
    user_scores : List[UserScores]
    
    class Config:
        from_attributes = True