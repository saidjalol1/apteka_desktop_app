from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from database_config.database_conf import get_db

import pydantic_models
from auth import auth_main
from database_models import models
from .pydantic_profile import Profile

app = APIRouter(
     tags=["Kassir Routerlari"]
)


@app.get("/profile/", name="profil")
async def cashier(start_date: date = Query(None), end_date: date = Query(None),
    current_user: models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == current_user.id).options(joinedload(models.UserSalaries.giver)).all()
    profile_data = {"user": user,"user_salaries": user_salaries}
    return profile_data


@app.put("/profile/edit")
async def profile_edit(user_update: pydantic_models.models.UserEdit,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.post("/sale/choosed/")
async def sale(sale_item: pydantic_models.models.SaleItemIn,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    sale_item = models.SaleItem(**sale_item)
    db.add(sale_item)
    db.commit()
    db.refresh(sale_item)
    return {"message": "success"}


