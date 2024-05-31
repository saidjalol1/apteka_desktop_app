from fastapi import FastAPI

app = FastAPI()

from database_config.database_conf import SessionLocal,engine, get_db, Base
from database_models.product_model import Base


Base.metadata.create_all(bind=engine)


@app.get("/")
async def sale():
    return {"message"}