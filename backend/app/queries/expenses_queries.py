from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets, Contacts, Transactions, Relationships, Categories
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr
import app.helpers


# This file holds all my CRUD queries that is related users expenses

def insert_new_expense_into_db(user_id, year, month, day, amount, category_id, note):
    
    amount = app.helpers.convert_float_to_int(amount)

    new_expense = UsersSpendings(user_id=user_id, date=datetime(year, month, day), amount_spent=amount, category_id=category_id, note=note)
    
    db.session.add(new_expense)
    
    db.session.commit()
    
def select_years_contains_expenses(user_id):
    
    years = UsersSpendings.query.with_entities(
                extract('year', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == user_id
            ).group_by(
                extract('year', UsersSpendings.date)
            ).order_by(
                extract('year', UsersSpendings.date).desc()
            ).all()
            
    # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
    years = [year[0] for year in years]
    
    return years

def select_most_recent_month(user_id, year):
    most_recent_month_list = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == user_id
                ).filter(
                    extract('year', UsersSpendings.date) == year
                ) .group_by(
                    extract('month', UsersSpendings.date)
                ).order_by(
                    extract('month', UsersSpendings.date).desc()
                ).first()
                
    most_recent_month = most_recent_month_list[0]
    
    return most_recent_month

def select_all_months_contain_expenses_in_specific_year(user_id, year):
    months = UsersSpendings.query.with_entities(
                extract('month', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == user_id
            ).filter(
                extract('year', UsersSpendings.date) == year
            ) .group_by(
                extract('month', UsersSpendings.date)
            ).order_by(
                extract('month', UsersSpendings.date).desc()
            ).all()
    
    return months

def select_expenses_in_month(user_id, year, month):
    
    month_expenses = db.session.query(UsersSpendings, Categories.name).join(Categories, UsersSpendings.category_id == Categories.id).filter(UsersSpendings.user_id == user_id, extract('year', UsersSpendings.date) == year, extract('month', UsersSpendings.date) == month).order_by(UsersSpendings.spending_id.desc()).all()
    
    return month_expenses

def extract_total_amount_of_month_expenses(user_id, year, month):
    
    total_amount_of_month_expenses = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == user_id).filter(extract('year', UsersSpendings.date) == year).filter(extract('month', UsersSpendings.date) == month).scalar()
    
    return total_amount_of_month_expenses

