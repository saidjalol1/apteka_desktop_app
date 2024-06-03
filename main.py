from fastapi import FastAPI
from database_config.database_conf import SessionLocal,engine, get_db
from database_models.product_model import Base 

from routes import cashier_route

app = FastAPI()

#Route Registery
app.include_router(cashier_route.app)




Base.metadata.create_all(bind=engine)




@app.get("/")
async def sale():
    return {"message"}