from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr
import app.helpers


# This file holds all my CRUD queries that is related users expenses

def insert_new_expense_into_db(user_id, year, month, day, amount, category):
    
    amount = app.helpers.convert_float_to_int(amount)

    new_expense = UsersSpendings(user_id=user_id, date=datetime(year, month, day), amount_spent=amount, category=category)
    
    db.session.add(new_expense)
    
    db.session.commit()
    
    