import os
from datetime import date, timedelta
from typing import Annotated, Optional, List
from fastapi import APIRouter, Body, HTTPException, status,Depends, Query, File, Form, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, and_, extract
from database_config.database_conf import get_db, current_time
from pydantic_models import product_models, user_models, sale_models, salary_models
from database_models import models
from auth import password, auth_main
from crud import product_fetch_crud
from my_util_functions.profile_util_functions import sale_statistics, top_10_products_statistics, workers_tabel, reports, get_sales_with_details, save_logo, generate_qr_code
from fastapi.encoders import jsonable_encoder


database_dep : Session = Depends(get_db)
current_user_dep : user_models.User = Depends(auth_main.get_current_user)


app = APIRouter(
    prefix= "/admin",
    tags= ["Admin routes"]
)


@app.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(userin : user_models.CreateUser,current_user = current_user_dep,database = database_dep):
    try:
        user = models.User(**userin.model_dump())
        user.hashed_password = password.pwd_context.hash(userin.hashed_password)
        database.add(user)  
        database.commit()
        database.refresh(user)
        return {"message": "success"}
    except:
        return {"message":"There is a user with this username"}
    

@app.post("/create_admin/", status_code=status.HTTP_201_CREATED, name="create admin")
async def create_user(userin : user_models.CreateUser,database = database_dep):
    user = models.User(**userin.model_dump())
    user.hashed_password = password.pwd_context.hash(userin.hashed_password)
    database.add(user)
    database.commit()
    database.refresh(user)
    return {"message": "success"}


@app.post("/salary/")
async def salary_give(salary :salary_models.SalaryInModel,current_user = current_user_dep,database = database_dep):
    if current_user.is_admin:
        slary = models.UserSalaries(**salary.model_dump())
        slary.giver_id = current_user.id
        slary.type = "oylik"
        database.add(slary)
        database.commit()
        database.refresh(slary)
        return {"message": "success"}
    else:
        return {"error":"only admin can access this route"}


@app.get("/users/", response_model=List[user_models.UserOut])
async def users_get(db = database_dep):
    users = db.query(models.User).all()
    return users

# Product Routes
@app.post("/product/create")
async def create_product(product: product_models.ProductIn,current_user = current_user_dep,database = database_dep):
    if current_user.is_admin:
        return product_fetch_crud.create(database,product)
    else:
        return {"error":"only admin can access this route"}



@app.post("/shift/add")
async def create_shift(shift:user_models.ShiftIn,current_user = current_user_dep,database = database_dep):
    shift_object = models.UserShift(**shift.model_dump())
    database.add(shift_object)
    database.commit()
    database.refresh(shift_object)
    return {"message":"seccess"}


@app.get("/shifts/", response_model=List[user_models.UserShiftOut])
async def shifts(current_user = current_user_dep,database = database_dep):
    shifts = database.query(models.UserShift).all()
    return shifts


@app.get("/category/", response_model=List[product_models.CategoryOut])
async def shifts(current_user = current_user_dep,database = database_dep):
    category = database.query(models.Category).all()
    return category


@app.post("/category/add")
async def create_shift(shift:product_models.CategoryIn,current_user = current_user_dep,database = database_dep):
    categiry_object = models.Category(**shift.model_dump())
    database.add(categiry_object)
    database.commit()
    database.refresh(categiry_object)
    return {"message":"seccess"}


@app.get("/workers/")
async def workers(start_date: Optional[date] = None, end_date : Optional[date] = None,
    filter: Optional[str] = Query("today", description="Filter criteria: Бугун, Бу ҳафта, Бу ойда, Бу квартал"),
    current_user = current_user_dep,database = database_dep):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can view worker statistics")
    results =  workers_tabel(database,start_date, end_date, filter)
    return {"result": results}
    
    
@app.get("/statistics/")
async def statistcs(current_user = current_user_dep,database = database_dep):
    context = sale_statistics(database)
    top_10_products = top_10_products_statistics(database)
    workers_table =  workers_tabel(database)
    return {"graph_objects": context, "top_10_products": top_10_products, "workers_table":workers_table}


@app.get("/reports/")
async def report(start_date: Optional[date] = None, end_date : Optional[date] = None,
    filter: Optional[str] = Query("thismonth", description="Filter criteria: Бугун, Бу ҳафта, Бу ойда, Бу квартал"),
    current_user = current_user_dep,database = database_dep):
    graph_data = reports(database, start_date, end_date, filter)
    table_data = top_10_products_statistics(database, start_date, end_date, filter)
    return {"graph_data":graph_data, "table_data":table_data}


@app.get("/retail/")
async def retail(start_date: Optional[date] = None, end_date : Optional[date] = None,
    filter: Optional[str] = Query("thismonth", description="Filter criteria: Бугун, Бу ҳафта, Бу ойда, Бу квартал"),
    current_user = current_user_dep,database = database_dep):
    context = get_sales_with_details(database, start_date, end_date, filter)
    return context


@app.post("/check-layout/")
async def create_check_layout(
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    shift_id: int = Form(...),
    logo: UploadFile = File(...),
    database = database_dep):
    try:
        logo_path = None
        if logo:
            logo_filename = logo.filename
            logo_data = await logo.read()
            logo_path = save_logo(logo_data, logo_filename)

        db_check_layout = models.CheckLayout(
            name=name,
            logo=logo_path,
            image=logo_path,  # Assuming image and logo are the same in your model
            phone=phone,
            address=address,
            shift_id=shift_id
        )
        database.add(db_check_layout)
        database.commit()
        database.refresh(db_check_layout)

        return {"message": "success"}

    except Exception as e:
        print(e)
        return {"message":"error"}
    

@app.post("/discount-card/create", response_model=sale_models.DiscountCardOut)
async def create_discount_card(
    obj : sale_models.DiscountCardIn,
    current_user = current_user_dep,
    db = database_dep
):
    try:
        # Create a new discount card
        new_card = models.DiscountCard(
            number=obj.number,
            amount=obj.amount,
            name=obj.name,
            surname=obj.surname
        )
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        # Generate a QR code
        qr_code_filename = f"{obj.number}.png"
        qr_code_path = os.path.join("static/qrcodes/", qr_code_filename)
        generate_qr_code(new_card.id, qr_code_path)
        new_card.qr_code_image = qr_code_path

        # Save the discount card to the database
        db.commit()
        db.refresh(new_card)

        return new_card
    except Exception as e:
        return {"message": e}

@app.get("/discount-cards/", response_model= List[sale_models.DiscountCardOut])
async def create_discount_card(
    current_user = current_user_dep,
    db = database_dep
):
   objs = db.query(models.DiscountCard).all()
   return objs

@app.get("/card/", )
async def create_discount_card(
    card_id : int,
    current_user = current_user_dep,
    db = database_dep
):
   dicts = {}
   if card_id > 0:
        objs = db.query(models.DiscountCard).filter(models.DiscountCard.id == card_id).first()
        dicts  = {
            "id": objs.id,
            "amount" : objs.amount,
            "name": objs.name,
            "number" : objs.number,
            "qr_code_image" : objs.qr_code_image,
            "surname" : objs.surname,
            }
   return dicts