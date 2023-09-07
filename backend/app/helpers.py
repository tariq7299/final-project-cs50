from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr



# It formats any number given to a Egypting currency format
def egp(value):
    """Format value as USD."""
    return f"{value:,.2f} EGP"

# This converts money values stored in db as int(amount*100) to float by doing amount/100.
"""
Because money amounts are stored as int(amount*100) we have to convert it back to float, before displaying it on user screen.
And also notice that I'm doing so because money columns stored in my db models as "Integer" not "Numaric" or "REAL" becasue after searching and asking GPT and bing, it seems that "Integer" data type is much better for storing money values.
"""
def convert_int_to_float(amount):
    return egp(amount/100)

