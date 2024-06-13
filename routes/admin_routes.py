from datetime import date, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Body, HTTPException, status,Depends, Query   
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, and_, extract
from database_config.database_conf import get_db, current_time

import pydantic_models
from database_models import models
from auth import password, auth_main
from crud import product_fetch_crud


app = APIRouter(
    prefix= "/admin",
    tags= ["Admin routes"]
)

@app.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(userin : pydantic_models.models.CreateUser,current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    if current_user.is_admin:
        user = models.User(
            username = userin.username,
            hashed_password = password.pwd_context.hash(userin.password),
            is_admin = userin.is_admin,
    
            first_name = userin.first_name,
            last_name = userin.last_name,
            born_date = userin.born_date,
            phone_number = userin.phone_number,
            address = userin.address,
            shift = userin.shift
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        print(current_user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can create user")
    return {"message": "success"}
    

@app.post("/create_admin/", status_code=status.HTTP_201_CREATED, name="create admin")
async def create_user(userin : pydantic_models.models.CreateUser,db: Session = Depends(get_db)):
    user = models.User(
        username = userin.username,
        hashed_password = password.pwd_context.hash(userin.password),
        is_admin = userin.is_admin,
    
        first_name = userin.is_admin,
        last_name = userin.last_name,
        born_date = userin.born_date,
        phone_number = userin.phone_number,
        address = userin.address,
        shift = userin.shift
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "success"}


@app.post("/salary/")
async def salary_give(salary : pydantic_models.models.SalaryInModel,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    if current_user.is_admin:
        slary = models.UserSalaries(
            amount = salary.amount,
            type = salary.type,
            date_received = salary.date_received,
            receiver_id = salary.receiver_id,
            giver_id = current_user.id
        )
        db.add(slary)
        db.commit()
        db.refresh(slary)
        return {"message": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can create user")

# Product Routes
@app.post("/product/create", response_model=pydantic_models.models.ProductOut)
async def create_product(product: pydantic_models.models.ProductIn,current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db:Session = Depends(get_db)):
    if current_user.is_admin:
        product = product_fetch_crud.create(db,product)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can add product")
    return product


@app.put("/product/edit")
async def product_edit(product_id : int,product_update: pydantic_models.models.ProductIn,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    if current_user.is_admin:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can edit product")


# @app.put("/product/delete")
# async def product_delete(product_id : int, 
#     current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
#     if current_user.is_admin:
#         product = db.query(models.Product).filter(models.Product.id == product_id).first()
#         if not product:
#             raise HTTPException(status_code=404, detail="Product not found")
        
#         db.delete(product)
#         db.commit()
#         return product
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can delete product")

# Helper function to get the start date of the current quarter
def get_current_quarter_start_date():
    today = current_time().date().today()
    quarter = (today.month - 1) // 3 + 1
    return date(today.year, 3 * quarter - 2, 1)

@app.get("/workers/")
async def workers(start_date: Optional[date] = None, end_date : Optional[date] = None,
    filter: Optional[str] = Query("today", description="Filter criteria: Бугун, Бу ҳафта, Бу ойда, Бу квартал"),
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),
    db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can view worker statistics")

    today = current_time().date()
    if start_date and end_date:
        pass
    elif filter == "today":
        start_date = today
        end_date = today
    elif filter == "thisweek":
        start_date = today - timedelta(days=today.weekday())
        end_date = today
        print(start_date, end_date)
    elif filter == "thismonth":
        start_date = date(today.year, today.month, 1)
        end_date = today
    elif filter == "thisquarter":
        start_date = get_current_quarter_start_date()
        end_date = today
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filter criteria")

    # Debugging print statements
    print(f"Filter: {filter}")
    print(f"Start Date: {start_date}, End Date: {end_date}")

    # Fetch statistics for the given date range 
    table = []
    workers = db.query(models.User).filter(models.User.is_admin == False).all()
    for i in workers:
        user_sale_ = db.query(models.Sale).filter(models.Sale.status == "sotilgan").filter(models.Sale.owner_id == i.id).filter(and_(\
                                    extract('year', models.Sale.date_added) >= start_date.year,
                                    extract('month', models.Sale.date_added) >= start_date.month,
                                    extract('day', models.Sale.date_added) >= start_date.day,
                                    extract('year', models.Sale.date_added) <= end_date.year,
                                    extract('month', models.Sale.date_added) <= end_date.month,
                                    extract('day', models.Sale.date_added) <= end_date.day,
                                )).all()
        user_sale_count = 0
        for d in user_sale_:
            user_sale_count += 1
        user_scores = db.query(func.sum(models.UserScores.score)).\
                                filter(models.UserScores.owner_id == i.id).\
                                filter(and_(
                                    extract('year', models.UserScores.date_scored) >= start_date.year,
                                    extract('month', models.UserScores.date_scored) >= start_date.month,
                                    extract('day', models.UserScores.date_scored) >= start_date.day,
                                    extract('year', models.UserScores.date_scored) <= end_date.year,
                                    extract('month', models.UserScores.date_scored) <= end_date.month,
                                    extract('day', models.UserScores.date_scored) <= end_date.day,
                                )).\
                                scalar()
        avans = db.query(func.sum(models.UserSalaries.amount)).\
                                filter(models.UserSalaries.receiver_id == i.id).\
                                filter(models.UserSalaries.type == "avans").\
                                filter(and_(
                                    extract('year', models.UserSalaries.date_received) >= start_date.year,
                                    extract('month', models.UserSalaries.date_received) >= start_date.month,
                                    extract('day', models.UserSalaries.date_received) >= start_date.day,
                                    extract('year', models.UserSalaries.date_received) <= end_date.year,
                                    extract('month', models.UserSalaries.date_received) <= end_date.month,
                                    extract('day', models.UserSalaries.date_received) <= end_date.day,
                                )).\
                                scalar()       
                                
        user_salaries = db.query(func.sum(models.UserSalaries.amount)).\
                                filter(models.UserSalaries.receiver_id == i.id).\
                                filter(models.UserSalaries.type == "oylik").\
                                filter(and_(
                                    extract('year', models.UserSalaries.date_received) >= start_date.year,
                                    extract('month', models.UserSalaries.date_received) >= start_date.month,
                                    extract('day', models.UserSalaries.date_received) >= start_date.day,
                                    extract('year', models.UserSalaries.date_received) <= end_date.year,
                                    extract('month', models.UserSalaries.date_received) <= end_date.month,
                                    extract('day', models.UserSalaries.date_received) <= end_date.day,
                                )).\
                                scalar()
        user_bonus = db.query(func.sum(models.UserSalaries.amount)).\
                                filter(models.UserSalaries.receiver_id == i.id).\
                                filter(models.UserSalaries.type == "bonus").\
                                filter(and_(
                                    extract('year', models.UserSalaries.date_received) >= start_date.year,
                                    extract('month', models.UserSalaries.date_received) >= start_date.month,
                                    extract('day', models.UserSalaries.date_received) >= start_date.day,
                                    extract('year', models.UserSalaries.date_received) <= end_date.year,
                                    extract('month', models.UserSalaries.date_received) <= end_date.month,
                                    extract('day', models.UserSalaries.date_received) <= end_date.day,
                                )).\
                                scalar()               

        table.append({
            "worker": i.first_name + ' ' + i.last_name,
            "user_sale_count":user_sale_count,
            "user_scores":user_scores,
            "avans":avans,
            "user_salaries":user_salaries,
            "user_bonus":user_bonus
        })
        
   

    return {
        "Ишчилар статистикаси": table
    }