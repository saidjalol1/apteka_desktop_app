from fastapi import APIRouter

cashier = APIRouter(
    tags="Kassir"
)



@cashier.get("cashier/")
async def cashier():
    products = 
    return 