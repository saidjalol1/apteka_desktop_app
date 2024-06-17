from datetime import timedelta, datetime
from typing import Annotated, Optional
from sqlalchemy import extract
from sqlalchemy.orm import Session, joinedload
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

from database_models import models
from crud import product_fetch_crud
from auth import auth_main, password, token

from pydantic_models import user_models, salary_models, product_models, sale_models
from routes import cashier_route, admin_routes
from database_config.database_conf import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


database_dep : Session = Depends(get_db)
current_user_dep : user_models.User = Depends(auth_main.get_current_user)

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "http://localhost:3000/",
#     "http://example.com",  # Replace with your actual front-end URL
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#Route Registery
app.include_router(cashier_route.app)
app.include_router(admin_routes.app)
models.Base.metadata.create_all(bind=engine)

# Get the current month and year
current_month = datetime.now().month
current_year = datetime.now().year



@app.get("/")
async def welcome():
    return {"message":"Wlecome"}


@app.get("/home")
async def home(
        check_id : Optional[int] = None,
        skip: int = 0, limit: int = 10,
        current_user = current_user_dep,database = database_dep):
    
    products = product_fetch_crud.get_products(database, skip, limit)
    user_scores = (database.query(models.UserScores).filter(models.UserScores.owner_id == current_user.id,
        extract('month', models.UserScores.date_scored) == current_month,
        extract('year', models.UserScores.date_scored) == current_year).all())
    this_month_score = sum(score.score for score in user_scores)
    items = []
    if check_id:
       check =  database.query(models.Sale).filter(models.Sale.id == check_id).first()
       items = database.query(models.SaleItem).filter(models.SaleItem.sale_id == check_id).all()
    else:
        check = models.Sale(
            amount = 0,
            status = "active",
            owner_id = current_user.id
        )
        database.add(check)
        database.commit()
        database.refresh(check)
    response_check_model = sale_models.CheckOut.model_validate(check)
    response_items = [ sale_models.SaleItemOut.model_validate(item) for item in items]
    response_products = [ product_models.ProductOut.model_validate(product) for product in products]
    object = {
        "products": response_products,
        "this_month_score": this_month_score,
        "check": response_check_model,
        "items": response_items
    }
    return object


@app.get("/sell")
async def sell(
        check_object : sale_models.Sell,
        current_user = current_user_dep,database = database_dep):
    try:
        check = database.query(models.Sale).filter(models.Sale.id == check_object.check_id).filter(models.Sale.owner_id == current_user.id).first()
        check.status = "sotilgan"
        check.amount = check_object.total
        check.payment_type = check_object.payment_type
    
        database.commit()
        database.refresh(check)
        return {"message": "success"}
    except Exception as e:
        print(e)
        return e


# @app.get("/return")
# async def sell(
#         check_id : int,
#         current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),
#         db: Session = Depends(get_db)):
#     try:
#         check = db.query(models.Sale).filter(models.Sale.id == check_id).filter(models.Sale.owner_id == current_user.id).first()
#         check.status = "sotilgan"
    
#         db.commit()
#         db.refresh(check)
#     except Exception as e:
#         print(e)
#         return e
#     return {"message": "success"}

# @app.post("/token/")
# async def login(user_token : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
#     try:
#         user = auth_main.authenticate_user(user_token.username,user_token.password, db)
#         print(user)
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validated the User")
#         created_token = token.create_access_token(user.username, user.id, timedelta(minutes=1000))
#         return {"access_token": created_token, "token_type": "bearer", "is_admin":user.is_admin}
#     except Exception as e:
#         return {"error": e}


@app.post("/token/")
async def login(user_token : user_models.UserLogin,database = database_dep):
    try:
        user = auth_main.authenticate_user(user_token.username,user_token.password, database)
        print(user)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validated the User")
        created_token = token.create_access_token(user.username, user.id, timedelta(minutes=1000))
        return {"access_token": created_token, "token_type": "bearer", "is_admin":user.is_admin}
    except Exception as e:
        return {"error": e}


