import os
import qrcode
import datetime
from datetime import date, timedelta
from fastapi import HTTPException, status
from database_models import models
from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session, joinedload
from database_config.database_conf import  current_time
from dateutil.relativedelta import relativedelta


today_date = current_time().date()
first_day_of_current_month = today_date.replace(day=1)


first_day_of_last_month = (first_day_of_current_month - relativedelta(months=1)).replace(day=1)
last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)


def get_current_quarter_start_date():
    today = current_time().date().today()
    quarter = (today.month - 1) // 3 + 1
    return date(today.year, 3 * quarter - 2, 1)


def user_score_retrieve(user_id, db, date=None, this_month=None, start_date=None, end_date=None):
    if start_date and end_date:
        query = db.query(models.UserScores)\
                .options(joinedload(models.UserScores.item))\
                .filter(models.UserScores.owner_id == user_id).filter(
            models.UserScores.date_scored >= start_date,
            models.UserScores.date_scored <= end_date
        ).all()

    elif this_month:
        query = db.query(models.UserScores)\
                .options(joinedload(models.UserScores.item))\
                .filter(models.UserScores.owner_id == user_id).filter(
            extract('year', models.UserScores.date_scored) == this_month.year,
            extract('month', models.UserScores.date_scored) == this_month.month,
        ).all()

    elif date:
        query =  db.query(models.UserScores)\
                .options(joinedload(models.UserScores.item))\
                .filter(models.UserScores.owner_id == user_id).filter(
                    extract('year', models.UserScores.date_scored) == date.year,
                    extract('month', models.UserScores.date_scored) == date.month,
                    extract('day', models.UserScores.date_scored) == date.day
                ).all()
    else:
        query = db.query(models.UserScores)\
                .options(joinedload(models.UserScores.item))\
                .filter(models.UserScores.owner_id == user_id).all()
    
    if not query:
        return {"message": "There is no score for this user"}
    
    serialized_scores = []
    for score in query:
        item = score.item
        if item and item.sale_product_items:
            product = item.sale_product_items
            score_dict = {
                'score': score.score,
                'date_scored': score.date_scored.date(),
                'item': {
                    'id': item.id,
                    'amount_of_box': item.amount_of_box,
                    'amount_of_package': item.amount_of_package,
                    'amount_from_package': item.amount_from_package,
                    'total_sum': item.total_sum,
                    'product_id': item.product_id,
                    'sale_id': item.sale_id,
                    'sale_product_items': {
                        'id': product.id,
                        'serial_number': product.serial_number,
                        'name': product.name,
                        'sale_price': product.sale_price,
                        'box': product.box,
                        'amount_in_box': product.amount_in_box,
                        'amount_in_package': product.amount_in_package,
                        'produced_location': product.produced_location,
                        'expiry_date': product.expiry_date,
                        'score': product.score
                    }
                }
            }
            serialized_scores.append(score_dict)
    
    return serialized_scores


def today_user_score(user_id, db):
    scores = db.query(models.UserScores)\
            .options(joinedload(models.UserScores.item))\
            .filter(models.UserScores.owner_id == user_id).filter(and_(\
                                    extract('year', models.Sale.date_added) == today_date.year,
                                    extract('month', models.Sale.date_added) == today_date.month,
                                    extract('day', models.Sale.date_added) == today_date.day
                                )).all()
    return scores


def user_salaries(user_id, db, date=None, this_month=None, start_date=None, end_date= None):
    if date:
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).options(joinedload(models.UserSalaries.giver)).filter(and_(\
                                    extract('year', models.UserSalaries.date_received) == date.year,
                                    extract('month', models.UserSalaries.date_received) == date.month,
                                    extract('day', models.UserSalaries.date_received) == date.day
                                )).all()
    elif this_month:
        print(this_month)
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).options(joinedload(models.UserSalaries.giver)).filter(and_(\
                                    extract('year', models.UserSalaries.date_received) == this_month.year,
                                    extract('month', models.UserSalaries.date_received) == this_month.month,
                                )).all()
    
    elif start_date and end_date:
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).filter(models.UserSalaries.date_received >= start_date,models.UserSalaries.date_received <= end_date).options(joinedload(models.UserSalaries.giver)).all()
    else:
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).options(joinedload(models.UserSalaries.giver)).all()
        
    salaries_list = []
    for salary in user_salaries:
        salary_dict = {
            'salary_id': salary.id,
            'amount': salary.amount,
            'type': salary.type,
            'date_received': salary.date_received.date(),
            'giver_username': salary.giver.username if salary.giver else None,
            'giver_first_name': salary.giver.first_name if salary.giver else None,
            'giver_last_name': salary.giver.last_name if salary.giver else None,
            'receiver_username': salary.receiver.username if salary.receiver else None,
            'receiver_first_name': salary.receiver.first_name if salary.receiver else None,
            'receiver_last_name': salary.receiver.last_name if salary.receiver else None,
        }
        salaries_list.append(salary_dict)
    
    return salaries_list


def calculate_percent_change(current_value, previous_value):
    # Handle case where previous_value is 0
    if previous_value == 0:
        # If both current_value and previous_value are 0, return None
        if current_value == 0:
            return 0
        else:
            # If previous_value is 0 and current_value is non-zero, return infinity
            return 0
    
    # Calculate percentage change for normal case
    percent_change = ((current_value - previous_value) / previous_value) * 100
    return percent_change


def sale_statistics(session):
    # Overall sum of sales for the current month
    overall_sum_sales_current_month = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month
    )).scalar() or 0

    # Overall profit for the current month
    overall_profit_current_month = session.query(
        func.sum((models.Product.sale_price - models.Product.base_price) * models.SaleItem.amount_of_box)
    ).select_from(
        models.Sale
    ).join(
        models.SaleItem, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month
    )).scalar() or 0

     # Sum of salaries received by users in the current month
    overall_sum_salaries_current_month = session.query(
        func.sum(models.UserSalaries.amount)
    ).filter(and_(
        extract('year', models.UserSalaries.date_received) == today_date.year,
        extract('month', models.UserSalaries.date_received) == today_date.month
    )).scalar() or 0
    
    # Quantity of sales for the current month
    quantity_of_sales_current_month = session.query(
        func.count(models.Sale.id)
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month
    )).scalar() or 0

    # Sum of expance received by users in the last month
    overall_sum_expance_current_month = session.query(
        func.sum(models.UserExpances.amount)
    ).filter(and_(
        extract('year', models.UserExpances.date_added) == today_date.year,
        extract('month', models.UserExpances.date_added) == today_date.month
    )).scalar() or 0
    
    # Overall sum of sales for the last month
    overall_sum_sales_last_month = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month - 1
    )).scalar() or 0

    # Overall profit for the last month
    overall_profit_last_month = session.query(
        func.sum((models.Product.sale_price - models.Product.base_price) * models.SaleItem.amount_of_box)
    ).select_from(
        models.Sale
    ).join(
        models.SaleItem, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month - 1
    )).scalar() or 0

    # Quantity of sales for the last month
    quantity_of_sales_last_month = session.query(
        func.count(models.Sale.id)
    ).filter(and_(
        extract('year', models.Sale.date_added) == today_date.year,
        extract('month', models.Sale.date_added) == today_date.month - 1
    )).scalar() or 0

    # Sum of salaries received by users in the last month
    overall_sum_salaries_last_month = session.query(
        func.sum(models.UserSalaries.amount)
    ).filter(and_(
        extract('year', models.UserSalaries.date_received) == today_date.year,
        extract('month', models.UserSalaries.date_received) == today_date.month - 1
    )).scalar() or 0
    
    # Sales percentage change
    sales_percent_change = calculate_percent_change(overall_sum_sales_current_month, overall_sum_sales_last_month)

    # Profit percentage change
    profit_percent_change = calculate_percent_change(overall_profit_current_month, overall_profit_last_month)

    # Quantity of sales percentage change
    salary_change_percent = calculate_percent_change(overall_sum_salaries_current_month, overall_sum_salaries_last_month)
    
    # Quantity of sales percentage change
    quantity_sales_percent_change = calculate_percent_change(quantity_of_sales_current_month, quantity_of_sales_last_month)

    context = {
        "overall_sum_of_sale": round(overall_sum_sales_current_month),
        "overall_sum_of_profit": round(overall_profit_current_month),
        "quantity_of_sales_current_month": round(quantity_of_sales_current_month),
        "overall_sum_salaries_current_month": round(overall_sum_salaries_current_month),
        "overall_sum_expance_current_month": round(overall_sum_expance_current_month),
        # In Percent
        "salary_change_percent":round(salary_change_percent),
        "sales_percent_change": round(sales_percent_change),
        "profit_percent_change": round(profit_percent_change),
        "quantity_sales_percent_change": round(quantity_sales_percent_change)
    }

    return context


def reports(session, start_date=None, end_date=None, filter="thismonth"):
    today = current_time().date()
    if start_date and end_date:
        pass
    elif filter == "today":
        start_date = today
        end_date = today
    elif filter == "thisweek":
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif filter == "thismonth":
        start_date = date(today.year, today.month, 1)
        end_date = today
    elif filter == "thisquarter":
        start_date = get_current_quarter_start_date()
        end_date = today
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filter criteria")

    # Calculate the length of the selected period
    period_length = (end_date - start_date).days + 1

    # Define the comparison period
    last_period_start_date = start_date - timedelta(days=period_length)
    last_period_end_date = start_date - timedelta(days=1)

    # Overall sum of sales for the selected period
    overall_sum_sales_current_period = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date
    )).scalar() or 0

    # Overall profit for the selected period
    overall_profit_current_period = session.query(
        func.sum((models.Product.sale_price - models.Product.base_price) * models.SaleItem.amount_of_box)
    ).select_from(
        models.Sale
    ).join(
        models.SaleItem, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(and_(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date
    )).scalar() or 0

    # Sum of salaries received by users in the selected period
    overall_sum_salaries_current_period = session.query(
        func.sum(models.UserSalaries.amount)
    ).filter(and_(
        models.UserSalaries.date_received >= start_date,
        models.UserSalaries.date_received <= end_date
    )).scalar() or 0

    # Quantity of sales for the selected period
    quantity_of_sales_current_period = session.query(
        func.count(models.Sale.id)
    ).filter(and_(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date
    )).scalar() or 0

    # Sum of expenses received by users in the selected period
    overall_sum_expenses_current_period = session.query(
        func.sum(models.UserExpances.amount)
    ).filter(and_(
        models.UserExpances.date_added >= start_date,
        models.UserExpances.date_added <= end_date
    )).scalar() or 0

    # "Naqd savdo" (cash sales) for the selected period
    cash_sales_current_period = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date,
        models.Sale.payment_type == "naqd"
    )).scalar() or 0

    # "Nasiya savdo" (credit sales) for the selected period
    credit_sales_current_period = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date,
        models.Sale.payment_type == "nasiya"
    )).scalar() or 0

    # Overall sum of sales for the comparison period
    overall_sum_sales_last_period = session.query(
        func.sum(models.Sale.amount)
    ).filter(and_(
        models.Sale.date_added >= last_period_start_date,
        models.Sale.date_added <= last_period_end_date
    )).scalar() or 0

    # Overall profit for the comparison period
    overall_profit_last_period = session.query(
        func.sum((models.Product.sale_price - models.Product.base_price) * models.SaleItem.amount_of_box)
    ).select_from(
        models.Sale
    ).join(
        models.SaleItem, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(and_(
        models.Sale.date_added >= last_period_start_date,
        models.Sale.date_added <= last_period_end_date
    )).scalar() or 0

    # Quantity of sales for the comparison period
    quantity_of_sales_last_period = session.query(
        func.count(models.Sale.id)
    ).filter(and_(
        models.Sale.date_added >= last_period_start_date,
        models.Sale.date_added <= last_period_end_date
    )).scalar() or 0

    # Sum of salaries received by users in the comparison period
    overall_sum_salaries_last_period = session.query(
        func.sum(models.UserSalaries.amount)
    ).filter(and_(
        models.UserSalaries.date_received >= last_period_start_date,
        models.UserSalaries.date_received <= last_period_end_date
    )).scalar() or 0

    # Calculate percentage changes
    sales_percent_change = calculate_percent_change(overall_sum_sales_current_period, overall_sum_sales_last_period)
    profit_percent_change = calculate_percent_change(overall_profit_current_period, overall_profit_last_period)
    salary_change_percent = calculate_percent_change(overall_sum_salaries_current_period, overall_sum_salaries_last_period)
    quantity_sales_percent_change = calculate_percent_change(quantity_of_sales_current_period, quantity_of_sales_last_period)

    context = {
        "overall_sum_of_sale": round(overall_sum_sales_current_period),
        "overall_sum_of_profit": round(overall_profit_current_period),
        "quantity_of_sales_current_month": round(quantity_of_sales_current_period),
        "overall_sum_salaries_current_month": round(overall_sum_salaries_current_period),
        "overall_sum_expense_current_month": round(overall_sum_expenses_current_period),
        "naqd_savdo": round(cash_sales_current_period),
        "nasiya_savdo": round(credit_sales_current_period),
        "salary_change_percent": round(salary_change_percent),
        "sales_percent_change": round(sales_percent_change),
        "profit_percent_change": round(profit_percent_change),
        "quantity_sales_percent_change": round(quantity_sales_percent_change)
    }

    return context


def top_10_products_statistics(session, start_date=None, end_date=None, filter="thismonth"):
    today = current_time().date()
    if start_date and end_date:
        pass
    elif filter == "today":
        start_date = today
        end_date = today
    elif filter == "thisweek":
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif filter == "thismonth":
        start_date = date(today.year, today.month, 1)
        end_date = today
    elif filter == "thisquarter":
        start_date = get_current_quarter_start_date()
        end_date = today
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filter criteria")

    
    overall_sales_revenue = session.query(
        func.sum(models.Product.sale_price * models.SaleItem.amount_of_box).label('total_sales_revenue')
    ).join(
        models.SaleItem, models.SaleItem.product_id == models.Product.id
    ).join(
        models.Sale, models.Sale.id == models.SaleItem.sale_id
    ).filter(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date
    ).scalar()

    
    top_10_products = session.query(
        models.Product.name,
        func.sum(models.SaleItem.amount_of_box).label('quantity_sold'),
        func.sum(models.Product.sale_price * models.SaleItem.amount_of_box).label('total_sales')
    ).join(
        models.SaleItem, models.SaleItem.product_id == models.Product.id
    ).join(
        models.Sale, models.Sale.id == models.SaleItem.sale_id
    ).filter(
        models.Sale.date_added >= start_date,
        models.Sale.date_added <= end_date
    ).group_by(
        models.Product.id, models.Product.name
    ).order_by(
        func.sum(models.SaleItem.total_sum).desc() 
    ).limit(10)

    
    top_10_products_stats = top_10_products.all()

    
    product_statistics = []
    for product in top_10_products_stats:
        if product.quantity_sold > 0 and product.total_sales > 0:
            product_percentage_of_sales_revenue = (product.total_sales / overall_sales_revenue) * 100 if overall_sales_revenue else 0
            product_dict = {
                'product_name': product.name,
                'quantity_sold': product.quantity_sold,
                'total_sales': product.total_sales,
                'percentage_of_overall_sales_revenue': round(product_percentage_of_sales_revenue),
            }
            product_statistics.append(product_dict)
        else:
            pass

    return product_statistics


def workers_tabel(database,start_date=None, end_date=None, filter = "thismonth"):

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
    
    table = []
    workers = database.query(models.User).filter(models.User.is_admin == False).all()
    for i in workers:
        user_sale_ = database.query(models.Sale).filter(models.Sale.status == "sotilgan").filter(models.Sale.owner_id == i.id).filter(and_(\
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
        user_scores = database.query(func.sum(models.UserScores.score)).\
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
        avans = database.query(func.sum(models.UserSalaries.amount)).\
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
                                
        user_salaries = database.query(func.sum(models.UserSalaries.amount)).\
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
        user_bonus = database.query(func.sum(models.UserSalaries.amount)).\
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
        if user_sale_count > 0:
            table.append({
                "worker": i.first_name + ' ' + i.last_name,
                "user_sale_count":user_sale_count,
                "user_scores":user_scores,
                "avans":avans,
                "user_salaries":user_salaries,
                "user_bonus":user_bonus
            })
        
    return table


def get_sales_with_details(session: Session, start_date=None, end_date=None, filter="thismonth"):
    today = date.today()

    if start_date and end_date:
        pass
    elif filter == "today":
        start_date = today
        end_date = today
    elif filter == "thisweek":
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif filter == "thismonth":
        start_date = date(today.year, today.month, 1)
        end_date = today
    elif filter == "thisquarter":
        start_date = get_current_quarter_start_date()  # Implement this function according to your needs
        end_date = today
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filter criteria")

    # Query to get sales, their owners, and the user shift details for the selected period
    sales_with_details = session.query(
        models.Sale.id,
        models.Sale.amount,
        models.Sale.date_added,
        models.Sale.status,
        models.Sale.person,
        models.Sale.payment_type,
        models.UserShift.name.label('shift_name'),
        models.User.username.label('owner_username'),  # Alias to differentiate from 'owner_name'
        models.User.first_name.label('owner_first_name'),  # Additional user details
        models.User.last_name.label('owner_last_name'),  # Additional user details
        models.User.is_admin.label('user_type'),  # Additional user details
    ).join(
        models.User, models.User.id == models.Sale.owner_id
    ).join(
        models.UserShift, models.UserShift.id == models.User.shift_id
    ).filter(
        and_(
            models.Sale.status == "sotilgan",
            models.Sale.date_added >= start_date,
            models.Sale.date_added <= end_date
        )
    ).order_by(
        models.Sale.date_added.desc()  # Order by date added descending
    ).all()

    
    # Prepare the sales data in a list of dictionaries
    sales_statistics = []
    for sale in sales_with_details:
        sale_dict = {
            'sale_id': sale.id,
            'amount': sale.amount,
            'date_added': sale.date_added.date(),
            'person': sale.person,
            'status': sale.status,
            'payment_type': sale.payment_type,
            'owner_username': sale.owner_username,
            'owner_first_name': sale.owner_first_name,
            'owner_last_name': sale.owner_last_name,
            'user_type': "Admin" if sale.user_type == True else "Kassir",
            'shift_name': sale.shift_name
        }
        sales_statistics.append(sale_dict)
        print(sale_dict)
    return sales_statistics


def save_logo(logo_data: bytes, filename: str) -> str:
    upload_folder = os.path.join(os.getcwd(), "images")

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    logo_path = os.path.join(upload_folder, filename)

    with open(logo_path, "wb") as f:
        f.write(logo_data)

    return logo_path

def generate_qr_code(data: str, path: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)