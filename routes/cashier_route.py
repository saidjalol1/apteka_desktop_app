from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database_config.database_conf import get_db, current_time
from sqlalchemy import and_
import pydantic_models
from auth import auth_main
from database_models import models
from sqlalchemy import func
app = APIRouter(
     tags=["Kassir Routerlari"]
)



def user_score_retrieve(user_id, db, date=False):
    today_date = current_time().date()
    print(today_date)
    if date:
        scores = db.query(models.UserScores)\
               .options(joinedload(models.UserScores.item))\
               .filter(models.UserScores.owner_id == user_id)\
               .filter(models.UserScores.date_scored == today_date)\
               .all()
    else:
        scores = db.query(models.UserScores).options(joinedload(models.UserScores.item)).filter(models.UserScores.owner_id == user_id).all()
    serialize = []
    for score in scores:
        item = score.item
        print(score.date_scored)
        if item.sale_product_items:
            serialize.append(pydantic_models.models.UserScoreOut(
                score=score.score,
                date_scored=score.date_scored,
                item=pydantic_models.models.SaleItemOut(
                    id=item.id,
                    amount_of_box=item.amount_of_box,
                    amount_of_package=item.amount_of_package,
                    amount_from_package=item.amount_from_package,
                    total_sum=item.total_sum,
                    product_id=item.product_id,
                    sale_id=item.sale_id,
                    sale_product_items=pydantic_models.models.ProductOut(
                        id=item.sale_product_items.id,
                        serial_number=item.sale_product_items.serial_number,
                        name=item.sale_product_items.name,
                        sale_price=item.sale_product_items.sale_price,
                        box=item.sale_product_items.box,
                        amount_in_box=item.sale_product_items.amount_in_box,
                        amount_in_package=item.sale_product_items.amount_in_package,
                        produced_location=item.sale_product_items.produced_location,
                        expiry_date=item.sale_product_items.expiry_date,
                        score=item.sale_product_items.score
                    )
                )
            ))
    return serialize

@app.get("/profile/", name="profil")
async def cashier(start_date: date = Query(None), end_date: date = Query(None),
    current_user: models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    
    user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == current_user.id).options(joinedload(models.UserSalaries.giver)).all()
    user_scores = user_score_retrieve(current_user.id, db)
    today_user_retrieve = user_score_retrieve(current_user.id, db, date=True)
    today_score = sum([i.score for i in today_user_retrieve])
    print(today_user_retrieve)
    # if start_date and end_date:
    
    profile_data = {"user": current_user,"user_salaries": user_salaries, "user_scores":user_scores, "score_today":today_score}
    return profile_data


@app.put("/profile/edit")
async def profile_edit(user_update: pydantic_models.models.UserEdit,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        return {"error":"user not found"}
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


@app.post("/add_to_check/")
async def sale(sale_item_in: pydantic_models.models.SaleItemIn,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    sale_item = models.SaleItem(**sale_item_in.model_dump())
    product = db.query(models.Product).filter(models.Product.id == sale_item.product_id).first()
    if product:
        product.box -= sale_item.amount_of_box
    else:
        return {"error": "Mahsulot topilmadi"}
                            
    db.add(sale_item)
    db.commit()
    db.refresh(sale_item)
    
    count_drug = (sale_item.amount_of_box * sale_item.sale_product_items.amount_in_box) + sale_item.amount_of_package
    base_score = sale_item.sale_product_items.score / sale_item.sale_product_items.amount_in_package
    score = count_drug * base_score
    
    
    user_score = models.UserScores(
        score = score,
        owner_id = current_user.id,
        sale_item_id = sale_item.id
    )
    print(user_score)
    db.add(user_score)
    db.commit()
    db.refresh(user_score)
    return {"message": "success"}


# @app.put("/update_check_item/")
# async def sale(
#     sale_item_id : int,
#     sale_item_update: pydantic_models.models.SaleItemIn,
#     current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
#     sale_item = db.query(models.SaleItem).filter(models.SaleItem.id == sale_item_id).first()
#     if not sale_item:
#             raise HTTPException(status_code=404, detail="Product not found")
#     for key, value in sale_item_update.model_dump(exclude_unset=True).items():
#         setattr(sale_item, key, value)

#     db.commit()
#     db.refresh(sale_item)
#     return sale_item

@app.get("/user_scores/")
async def scores(current_user: pydantic_models.models.User = Depends(auth_main.get_current_user), db: Session = Depends(get_db)):
    scores = db.query(models.UserScores).options(joinedload(models.UserScores.item)).filter(models.UserScores.owner_id == current_user.id).all()
    serialize = []
    for score in scores:
        item = score.item
        if item.sale_product_items:
            serialize.append(pydantic_models.models.UserScoreOut(
                score=score.score,
                date_scored=score.date_scored,
                item=pydantic_models.models.SaleItemOut(
                    id=item.id,
                    amount_of_box=item.amount_of_box,
                    amount_of_package=item.amount_of_package,
                    amount_from_package=item.amount_from_package,
                    total_sum=item.total_sum,
                    product_id=item.product_id,
                    sale_id=item.sale_id,
                    sale_product_items=pydantic_models.models.ProductOut(
                        id=item.sale_product_items.id,
                        serial_number=item.sale_product_items.serial_number,
                        name=item.sale_product_items.name,
                        sale_price=item.sale_product_items.sale_price,
                        box=item.sale_product_items.box,
                        amount_in_box=item.sale_product_items.amount_in_box,
                        amount_in_package=item.sale_product_items.amount_in_package,
                        produced_location=item.sale_product_items.produced_location,
                        expiry_date=item.sale_product_items.expiry_date,
                        score=item.sale_product_items.score
                    )
                )
            ))
    return serialize

@app.delete("/delete_check_item/")
async def sale(
    sale_item_id : int,
    current_user: pydantic_models.models.User = Depends(auth_main.get_current_user),db: Session = Depends(get_db)):
    
    item = db.query(models.SaleItem).filter(models.SaleItem.id == sale_item_id).first()
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
        product.amount_in_box += item.amount_of_box
        
    user_scores = item.user_scores
    for user_score in user_scores:
        db.delete(user_score)
    if item:
        db.delete(item)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.commit()
    return {"message": "success"}


