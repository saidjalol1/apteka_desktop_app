from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database_config.database_conf import get_db, current_time
from sqlalchemy import func, and_, extract
from pydantic_models import user_models, product_models, sale_models, salary_models
from auth import auth_main
from database_models import models
from  my_util_functions.profile_util_functions import today_user_score, user_score_retrieve, user_salaries
today_date = current_time().date()

app = APIRouter(
     tags=["Kassir Routerlari"]
)


database_dep : Session = Depends(get_db)
current_user_dep : user_models.User = Depends(auth_main.get_current_user)


@app.get("/profile/", name="profil")
async def cashier(  date: Optional[date] = Query(None),
                    this_month: Optional[date] = Query(None),
                    start_date: Optional[date] = Query(None),
                    end_date: Optional[date] = Query(None),
                    current_user = current_user_dep,database = database_dep):
    # If date is not given
    user_salary = user_salaries(current_user.id,database)
    user_scores = user_score_retrieve(current_user.id, database)
    # If date is given
    if date:
        user_salary = user_salaries(current_user.id,database, date=date)
        user_scores = user_score_retrieve(current_user.id, database, date=date)
    elif this_month:
        user_salary = user_salaries(current_user.id,database,  this_month=this_month)
        user_scores = user_score_retrieve(current_user.id, database,  this_month=this_month)
    elif start_date and end_date:
        print(start_date, end_date)
        user_salary = user_salaries(current_user.id,database,  start_date=start_date, end_date=end_date)
        user_scores = user_score_retrieve(current_user.id, database,  start_date=start_date, end_date=end_date)
    else:
        pass
    overall_user_scores_retrieve = database.query(models.UserScores).filter(models.UserScores.owner_id == current_user.id).all()
    overall_user_score = sum([ i.score for i in overall_user_scores_retrieve])
    
    today_user_retrieve = today_user_score(current_user.id, database)
    today_score = sum([i.score for i in today_user_retrieve])
    
    user = database.query(models.User).filter(models.User.id == current_user.id).first()
    user_shift = database.query(models.UserShift).filter(models.UserShift.id == user.shift_id).first()
    
    user_sc = database.query(models.UserScores).filter(models.UserScores.owner_id == current_user.id)
    query = user_sc.filter(
            extract('year', models.UserScores.date_scored) == today_date.year,
            extract('month', models.UserScores.date_scored) == today_date.month,
        )
    
    scores = query.all()
    this_month_score = sum([ i.score for i in scores])
    if user:
        user  = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "type" : "Kassir" if user.is_admin == False else "Admin",
                    "born_date" : user.born_date,
                    "phone": user.phone_number,
                    "address" : user.address,
                    "shift": {
                        "id": user_shift.id if user_shift else 0,
                        "name": user_shift.name if user_shift else 'smenasi yo\'q'
                    }
                }
    else:
        return {"messsage":"User not found"}
    profile_data = {"user": user,"user_salaries": user_salary,"overall_user_score":overall_user_score,"this_month_score":this_month_score, "user_scores":user_scores, "score_today":today_score}
    return profile_data


@app.put("/profile/edit")
async def profile_edit(user_update: user_models.UserEdit,current_user = current_user_dep,database = database_dep):
    user = database.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        return {"error":"user not found"}
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    database.commit()
    database.refresh(user)
    return user


@app.post("/add_to_check/")
async def sale(sale_item_in: sale_models.SaleItemIn,current_user = current_user_dep,database = database_dep):
    sale_item = models.SaleItem(**sale_item_in.model_dump())
    product = database.query(models.Product).filter(models.Product.id == sale_item.product_id).first()
    if product:
        package = 0
        from_package = 0
        if sale_item_in.amount_of_package:
            package = sale_item_in.amount_of_package * product.amount_in_package 
        if sale_item_in.amount_from_package:
            from_package = sale_item_in.amount_from_package
        overall_for_sale = sum([package,from_package])
        sale_item.overall_for_sale = overall_for_sale
        print(overall_for_sale)
        if product.overall_amount >= overall_for_sale:
            product.overall_amount -= sum([package,from_package])
            database.commit()
            database.refresh(product)
            product.boxes_left = product.overall_amount // product.amount_in_package
            product.packages_left = product.overall_amount  % product.amount_in_package
            database.commit()
            database.refresh(product)
        else:
            return {"message":"Omborda Mahsulot Yetarli emas"}
    else:
        return {"message": "Mahsulot topilmadi"}
                            
    database.add(sale_item)
    database.commit()
    database.refresh(sale_item)
    return {"message": "success"}


@app.delete("/delete_check_item/")
async def sale(sale_item_id : int,current_user = current_user_dep,database = database_dep):
    
    item = database.query(models.SaleItem).filter(models.SaleItem.id == sale_item_id).first()
    product = database.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
        package = 0
        from_package = 0
        if item.amount_of_package:
            package = item.amount_of_package * product.amount_in_package 
        if item.amount_from_package:
            from_package = item.amount_from_package
        overall_for_sale = sum([package,from_package])
        item.overall_for_sale = overall_for_sale
        product.overall_amount += sum([package,from_package])
        database.commit()
        database.refresh(product)
        product.boxes_left = product.overall_amount // product.amount_in_package
        product.packages_left = product.overall_amount  % product.amount_in_package
        database.commit()
        database.refresh(product)
        database.delete(item)
        database.commit()
    else:
        return {"error":"Omborda Mahsulot yoki check item topilmadi Yetarli emas"}
    return {"message": "success"}


@app.post("/expance/add")
async def expance(expance: user_models.UserExpancesIn,current_user = current_user_dep, database = database_dep):
    try:
        expance_obj = models.UserExpances(**expance.model_dump())
        expance_obj.expance_owner_id = current_user.id
        database.add(expance_obj)
        database.commit()
        database.refresh(expance_obj)
    except Exception as e:
        print(e)
        return {"error": e}
    return {"message":"Success"}


@app.get("/expance/all", response_model= List[user_models.UserExpancesOut])
async def expance(current_user = current_user_dep, database = database_dep):
    try:
        expances = database.query(models.UserExpances).all()
        return expances
    except Exception as e:
        print(e)
        return {"error": e}
    

@app.post("/delay/check")
async def delay_check(check_id:int, db = database_dep):
    if check_id:
        obj = db.query(models.Sale).filter(models.Sale.id == check_id).first()
        for i in obj.items:
            product = db.query(models.Product).filter(models.Product.id == i.product_id).first()
            package = 0
            from_package = 0
            if i.amount_of_package:
                package = i.amount_of_package * product.amount_in_package 
            if i.amount_from_package:
                from_package = i.amount_from_package
            overall_for_sale = sum([package,from_package])
            i.overall_for_sale = overall_for_sale
            product.overall_amount += sum([package,from_package])
            db.commit()
            db.refresh(product)
            product.boxes_left = product.overall_amount // product.amount_in_package
            product.packages_left = product.overall_amount  % product.amount_in_package
            db.commit()
            db.refresh(product)

        db.delete(obj)
        db.commit()
        return {"message":"success"}
    else:
        return {"message":"Queriyda check id yo'q"}
