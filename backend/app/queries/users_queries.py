from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr
import app.helpers
import app.queries.users_queries
import app.queries.expenses_queries


# This file holds all my CRUD queries that is related users account


# THis fetch the user's wallet info (like: balance, debt, credit)
def get_user_wallet(user_id):
    
    # This SELECT the user's wallet from db
    wallet_class_instance  = db.session.query(UsersWallets).filter(UsersWallets.user_id == user_id).first()
    
    """
    Because money amounts are stored as int(amount*100) we have to convert it back to float, before displaying it on user screen.
    And also notice that I'm doing so because money columns stored in my db models as "Integer" not "Numaric" or "REAL" becasue after searching and asking GPT and bing, it seems that "Integer" data type is much better for storing money values.
    """
    wallet_class_instance.balance = app.helpers.convert_int_to_float(wallet_class_instance.balance)
    wallet_class_instance.debt = app.helpers.convert_int_to_float(wallet_class_instance.debt)
    wallet_class_instance.credit = app.helpers.convert_int_to_float(wallet_class_instance.credit)
    
    # Convert users' wallet row from 'class instance' to 'Dictionary', So to be able to jsonify() (So we can send it in the response as JSON), and access it in frontend.
    wallet = {'balance': wallet_class_instance.balance, 'debt': wallet_class_instance.debt, 'credit': wallet_class_instance.credit}
    
    return wallet