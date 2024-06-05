from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
import crud.product_fetch_crud
from database_config.database_conf import get_db


#My models for verification and Database access
import pydantic_models
from database_models.models import Product, UserScores, User, UserSalaries
from crud import product_fetch_crud
from auth import auth_main
from .pydantic_profile import Profile

app = APIRouter(
     tags=["Kassir Routerlari"]
)


@app.get("/profile/", name="profil")
async def cashier(start_date: date = Query(None), end_date: date = Query(None),
    current_user: User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    user_salaries = db.query(UserSalaries).filter(UserSalaries.receiver_id == current_user.id).options(joinedload(UserSalaries.giver)).all()
    profile_data = {"user": user,"user_salaries": user_salaries}
    return profile_data


@app.put("/profile/edit")
async def cshier_edit(user_update: pydantic_models.models.UserEdit,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.post("/sale/")
async def sale():
    return {"message": "success"}


