from datetime import timedelta, datetime
from typing import Annotated
from sqlalchemy import extract
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

import pydantic_models
import pydantic_models.models
from routes import cashier_route, admin_routes
from database_models import models
from crud import product_fetch_crud
from auth import auth_main, password, token
from database_config.database_conf import engine, get_db

app = FastAPI()

#Route Registery
app.include_router(cashier_route.app)
app.include_router(admin_routes.app)
models.Base.metadata.create_all(bind=engine)

# Get the current month and year
current_month = datetime.now().month
current_year = datetime.now().year


@app.get("/")
async def home(skip: int = 0, limit: int = 10,current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    products = product_fetch_crud.get_products(db, skip, limit)
    user_scores = (db.query(models.UserScores).filter(models.UserScores.owner_id == current_user.id,
        extract('month', models.UserScores.date_scored) == current_month,
        extract('year', models.UserScores.date_scored) == current_year).all())
    this_month_score = sum(score.score for score in user_scores)
    object = {
        "products": products,
        "this_month_score": this_month_score
    }
    return object


@app.post("/token/")
async def login(user_token : Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)):
    user = auth_main.authenticate_user(user_token.username,user_token.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validated the User")
    created_token = token.create_access_token(user.username, user.id, timedelta(minutes=1000))
    return {"access_token": created_token, "token_type": "bearer"}


