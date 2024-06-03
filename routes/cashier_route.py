from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud.product_fetch_crud
from database_config.database_conf import get_db


#My models for verification and Database access
from pydantic_models.models import BaseProduct
from database_models.product_model import Product

from crud import product_fetch_crud


app = APIRouter(
     tags=["Kassir Routerlari"]
)


@app.get("/cashier/" , response_model=list[BaseProduct], name="asosiy")
async def cashier(skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    products = product_fetch_crud.get_products(db, skip, limit)
    return products


@app.post("/product/create", response_model=BaseProduct)
async def create_product(product: BaseProduct,db:Session = Depends(get_db)):
    product = product_fetch_crud.create(db,product)
    return product