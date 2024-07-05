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


database_dep : Session = Depends(get_db)
current_user_dep : user_models.User = Depends(auth_main.get_current_user)
current_month = datetime.now().month
current_year = datetime.now().year


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


app.include_router(cashier_route.app)
app.include_router(admin_routes.app)
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def welcome():
    return {"message":"Wlecome"}


@app.get("/home")
async def home(
        check_id : Optional[int] = None,
        skip: int = 0, limit: int = 10,
        current_user = current_user_dep,database = database_dep):
    
    products = product_fetch_crud.get_products(database, skip, limit)
    user_scores = database.query(models.UserScores).filter(models.UserScores.owner_id == current_user.id).all()
    user_score = sum(score.score for score in user_scores)
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
    response_items = [sale_models.SaleItemOut.model_validate(item) for item in items]
    response_products = [ product_models.ProductOut.model_validate(product) for product in products]
    
    discount = sum([i.sale_product_items.discount_price for i in response_items])
    total = sum([ i.total_sum for i in response_items])
    payment = total - discount
    
    check.discount = discount
    check.amount = payment
    database.commit()
    database.refresh(check)
    
    check_object = {
        "total_discount": discount,
        "total": total,
        "payment" : payment
        }
    
    print(response_products)
    object = {
        "products": response_products,
        "user_scores": user_score,
        "check": response_check_model,
        "check_object": check_object,
        "items": response_items
    }
    return object


@app.post("/sell")
async def sell(
        check_object : sale_models.Sell,
        current_user = current_user_dep,database = database_dep):
        check = database.query(models.Sale).filter(models.Sale.id == check_object.check_id).filter(models.Sale.owner_id == current_user.id).first()
        items = database.query(models.SaleItem).filter(models.SaleItem.sale_id == check_object.check_id).all()
        check.status = "sotilgan"   
        check.amount = check_object.total
        check.discount = check_object.discount
        check.person = check_object.person
        check.payment_type = check_object.payment_type
        database.commit()
        database.refresh(check)
        
        if check_object.discount_card_id:
            card = database.query(models.DiscountCard).filter(models.DiscountCard.id == check_object.discount_card_id).first()
            if card:
                if check_object.with_discount_card:
                    if card.amount >= check_object.from_discount_card:
                        card.amount -= check_object.from_discount_card
                        database.commit()
                        database.refresh(card)
                    else:
                        return {"message":"Kartada yetarli pul mavjud emas"}
                else:
                    card.amount += check_object.discount
                    database.commit()
        
        for i in items:
            product = database.query(models.Product).filter(models.Product.id == i.product_id).first()
            box = product.amount_in_box *  product.amount_in_package * i.amount_of_box 
            package = product.amount_in_package * i.amount_of_package
            from_package = i.amount_from_package
            
            drug_count = sum([box, package,from_package])
            base_score = product.score / (product.amount_in_box * product.amount_in_package)
            score = drug_count * base_score
    
    
            user_score = models.UserScores(
                score = score,
                owner_id = current_user.id,
                sale_item_id = i.id
            )
            print(user_score.score)
            database.add(user_score)
            database.commit()
            database.refresh(user_score)
        
        return {"message": "success"}
    


@app.post("/cheque/")
async def cheque():
    message = {
        "message": "check_chiqarildi"
    }
    print(message)
    return message

    
@app.post("/remove_from_check/")
async def sale(sale_item_in: sale_models.ReturnIn,current_user = current_user_dep,database = database_dep):
    sale_item = models.ReturnItems(**sale_item_in.model_dump())
    product = database.query(models.Product).filter(models.Product.id == sale_item.product_id).first()
    if product:
        box = 0
        package = 0
        from_package = 0
        if sale_item_in.amount_of_box:
            box = product.amount_in_box *  product.amount_in_package * sale_item_in.amount_of_box 
        if sale_item_in.amount_of_package:
            package = product.amount_in_package * sale_item_in.amount_of_package
        if sale_item_in.amount_from_package:
            from_package = sale_item_in.amount_from_package
        overall_for_sale = sum([box, package,from_package])
        if product.overall_amount >= overall_for_sale:
            product.overall_amount += sum([box, package,from_package])
            product.box = product.overall_amount // (product.amount_in_box * product.amount_in_package)
        else:
            return {"message":"Omborda Mahsulot Yetarli emas"}
        print(box)
        print(package)
        print(from_package)
    else:
        return {"message": "Mahsulot topilmadi"}
                            
    database.add(sale_item)
    database.commit()
    database.refresh(sale_item)
    return {"message": "success"}


@app.delete("/delete_return_item/")
async def sale(return_item_id : int,current_user = current_user_dep,database = database_dep):
    item = database.query(models.ReturnItems).filter(models.ReturnItems.id == return_item_id).first()
    product = database.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
        box = 0
        package = 0
        from_package = 0
        if item.amount_of_box:
            box = product.amount_in_box *  product.amount_in_package * item.amount_of_box 
        if item.amount_of_package:
            package = product.amount_in_package * item.amount_of_package
        if item.amount_from_package:
            from_package = item.amount_from_package
        product.overall_amount -= sum([box, package,from_package])
        print([box, package,from_package])
        if box:
            product.box -= item.amount_of_box
        database.delete(item)
        database.commit()
    else:
        return {"error":"Omborda Mahsulot yoki check item topilmadi Yetarli emas"}
    return {"message": "success"}


@app.get("/return/")
async def home(
        return_id : Optional[int] = None,
        skip: int = 0, limit: int = 10,
        current_user = current_user_dep,database = database_dep):
    
    products = product_fetch_crud.get_products(database, skip, limit)
    items = []
    if return_id:
       check =  database.query(models.Return).filter(models.Return.id == return_id).first()
       items = database.query(models.ReturnItems).filter(models.ReturnItems.return_id == return_id).all()
    else:
        check = models.Return(
            amount = 0,
            discount = 0,
            owner_id = current_user.id
        )
        database.add(check)
        database.commit()
        database.refresh(check)
    response_check_model = sale_models.ResponceReturn.model_validate(check)
    response_items = [sale_models.ReturnOut.model_validate(item) for item in items]
    response_products = [ product_models.ProductOut.model_validate(product) for product in products]
    
    discount = sum([i.returned_items.discount_price for i in response_items])
    total = sum([ i.total_sum for i in response_items])
    payment = total - discount
    
    check.discount = discount
    check.amount = payment
    database.commit()
    database.refresh(check)
    
    check_object = {
        "total_discount": discount,
        "total": total,
        "payment" : payment
        }
    
    
    object = {
        "check": response_check_model,
        "check_object": check_object,
        "items": response_items,
        "products":response_products
    }
    return object


@app.post("/delay/return")
async def delay_check(check_id:int, db = database_dep):
    obj = db.query(models.Return).filter(models.Return.id == check_id).first()
    for i in obj.items:
        product = db.query(models.Product).filter(models.Product.id == i.product_id).first()
        box = 0
        package = 0
        from_package = 0
        if i.amount_of_box:
            box = product.amount_in_box *  product.amount_in_package * i.amount_of_box 
        if i.amount_of_package:
            package = product.amount_in_package * i.amount_of_package
        if i.amount_from_package:
            from_package = i.amount_from_package
        product.overall_amount += sum([box, package,from_package])
        print([box, package,from_package])
        if box:
            product.box += i.amount_of_box
        db.delete(i)
        db.commit()
    
    db.delete(obj)
    db.commit()
    return {"message":"success"}


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
