from fastapi import APIRouter, Body, HTTPException, status,Depends
from sqlalchemy.orm import Session
from database_config.database_conf import get_db

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
