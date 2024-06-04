from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import crud.product_fetch_crud
from database_config.database_conf import get_db


#My models for verification and Database access
import pydantic_models
from database_models.models import Product
from auth import auth_main
from crud import product_fetch_crud
from database_models.models import UserScores, User
from .pydantic_profile import Profile

app = APIRouter(
     tags=["Kassir Routerlari"]
)


@app.get("/profile/", name="profil")
async def cashier(start_date: date = Query(None), end_date: date = Query(None),
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    user_scores = db.query(UserScores).filter(UserScores.owner_id == current_user.id).all()
    user_scores_data = [{"id": score.id, "score": score.score} for score in user_scores]
    profile_data = {"user": user, "user_scores": user_scores_data}
    return profile_data


# @app.post("/product/create", response_model=BaseProduct)
# async def create_product(product: BaseProduct,db:Session = Depends(get_db)):
#     product = product_fetch_crud.create(db,product)
#     return product