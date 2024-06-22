import datetime
from datetime import date, timedelta
from fastapi import HTTPException, status
from database_models import models
from sqlalchemy import func, cast, Date, and_, extract
from sqlalchemy.orm import Session, joinedload
from database_config.database_conf import get_db, current_time
from pydantic_models import user_models, product_models, sale_models, salary_models
from dateutil.relativedelta import relativedelta


today_date = current_time().date()
first_day_of_current_month = today_date.replace(day=1)

# Calculate the first and last days of the previous month
first_day_of_last_month = (first_day_of_current_month - relativedelta(months=1)).replace(day=1)
last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)

# Helper function to get the start date of the current quarter
def get_current_quarter_start_date():
    today = current_time().date().today()
    quarter = (today.month - 1) // 3 + 1
    return date(today.year, 3 * quarter - 2, 1)

def user_score_retrieve(user_id, db, date=None):
    query = db.query(models.UserScores)\
              .options(joinedload(models.UserScores.item))\
              .filter(models.UserScores.owner_id == user_id)
    
    if date:
        query = query.filter(
            extract('year', models.UserScores.date_scored) == date.year,
            extract('month', models.UserScores.date_scored) == date.month,
            extract('day', models.UserScores.date_scored) == date.day
        )
    
    scores = query.all()
    
    serialize = []
    for score in scores:
        item = score.item
        if item.sale_product_items:
            serialize.append(user_models.UserScoreOut(
                score=score.score,
                date_scored=score.date_scored,
                item=sale_models.SaleItemOut(
                    id=item.id,
                    amount_of_box=item.amount_of_box,
                    amount_of_package=item.amount_of_package,
                    amount_from_package=item.amount_from_package,
                    total_sum=item.total_sum,
                    product_id=item.product_id,
                    sale_id=item.sale_id,
                    sale_product_items=sale_models.ProductOut(
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


def today_user_score(user_id, db):
    print(today_date , "Printed")
    scores = db.query(models.UserScores)\
            .options(joinedload(models.UserScores.item))\
            .filter(models.UserScores.owner_id == user_id).filter(and_(\
                                    extract('year', models.Sale.date_added) == today_date.year,
                                    extract('month', models.Sale.date_added) == today_date.month,
                                    extract('day', models.Sale.date_added) == today_date.day
                                )).all()
    return scores

def user_salaries(user_id, db, date=None):
    if date:
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).options(joinedload(models.UserSalaries.giver)).filter(and_(\
                                    extract('year', models.Sale.date_added) == date.year,
                                    extract('month', models.Sale.date_added) == date.month,
                                    extract('day', models.Sale.date_added) == date.day
                                )).all()
        return user_salaries
    else:
        user_salaries = db.query(models.UserSalaries).filter(models.UserSalaries.receiver_id == user_id).options(joinedload(models.UserSalaries.giver)).all()
        return user_salaries


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
        "overall_sum_of_sale": overall_sum_sales_current_month,
        "overall_sum_of_profit": overall_profit_current_month,
        "quantity_of_sales_current_month": quantity_of_sales_current_month,
        "overall_sum_salaries_current_month": overall_sum_salaries_current_month,
        "overall_sum_expance_current_month": overall_sum_expance_current_month,
        # In Percent
        "salary_change_percent":salary_change_percent,
        "sales_percent_change": sales_percent_change,
        "profit_percent_change": profit_percent_change,
        "quantity_sales_percent_change": quantity_sales_percent_change
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
        "overall_sum_of_sale": overall_sum_sales_current_period,
        "overall_sum_of_profit": overall_profit_current_period,
        "quantity_of_sales_current_month": quantity_of_sales_current_period,
        "overall_sum_salaries_current_month": overall_sum_salaries_current_period,
        "overall_sum_expense_current_month": overall_sum_expenses_current_period,
        "naqd_savdo": cash_sales_current_period,
        "nasiya_savdo": credit_sales_current_period,
        "salary_change_percent": salary_change_percent,
        "sales_percent_change": sales_percent_change,
        "profit_percent_change": profit_percent_change,
        "quantity_sales_percent_change": quantity_sales_percent_change
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

    # Query to get the top 10 products by quantity sold and their total sales for the selected period
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
        func.sum(models.SaleItem.amount_of_box).desc()  # Order by quantity sold descending
    ).limit(10)  # Limit to top 10 products

    # Execute the query and fetch all results
    top_10_products_stats = top_10_products.all()

    # Prepare the statistics in a list of dictionaries
    product_statistics = []
    for product in top_10_products_stats:
        if product.quantity_sold > 0 and product.total_sales > 0:
            product_dict = {
                'product_name': product.name,
                'quantity_sold': product.quantity_sold,
                'total_sales': product.total_sales,
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

    # Query to get sales, their owners, and the user shift details for the selected period
    sales_with_details = session.query(
        models.Sale.id,
        models.Sale.amount,
        models.Sale.date_added,
        models.Sale.status,
        models.Sale.payment_type,
        models.User.username.label('owner_name'),
        models.UserShift.name.label('shift_name')
    ).join(
        models.User, models.User.id == models.Sale.owner_id
    ).join(
        models.UserShift, models.UserShift.id == models.User.shift_id
    ).filter(
        and_(
            models.Sale.status == "sotilgan",
            extract('year', models.Sale.date_added) >= start_date.year,
            extract('month', models.Sale.date_added) >= start_date.month,
            extract('day', models.Sale.date_added) >= start_date.day,
            extract('year', models.Sale.date_added) <= end_date.year,
            extract('month', models.Sale.date_added) <= end_date.month,
            extract('day', models.Sale.date_added) <= end_date.day
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
            'date_added': sale.date_added,
            'status': sale.status,
            'payment_type': sale.payment_type,
            'owner_name': sale.owner_name,
            'shift_name': sale.shift_name
        }
        sales_statistics.append(sale_dict)

    return sales_statistics