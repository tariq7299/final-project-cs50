from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr
import requests
import uuid
from functools import wraps
from flask import redirect, render_template, session


def login_required(f):
    # This supposed to be @functools.wraps(f), this keeps the name and docstring of "f" function passed in decorated_function(*args, **kwargs), so without @functools.wraps(f), f.__name__ would change completely to decorated_function() instead of its correct __name__ which is in our case (login() or index(), history() ...etc)
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            response_object = { 'status': 'success', 'userNotLogged': True}
            return jsonify(response_object)
        return f(*args, **kwargs)
    return decorated_function

# It formats any number given to a Egypting currency format
def egp(amount):
    """Format value as USD."""
        # Becasue the amount can sometimes be a string, so I need to covert tot a number first
    amount = float(amount)
    return f"{amount:,.2f} EGP"

# This converts money values stored in db as int(amount*100) to float by doing amount/100.
"""
Because money amounts are stored as int(amount*100) we have to convert it back to float, before displaying it on user screen.
And also notice that I'm doing so because money columns stored in my db models as "Integer" not "Numaric" or "REAL" becasue after searching and asking GPT and bing, it seems that "Integer" data type is much better for storing money values.
"""
def convert_int_to_float(amount):
    # Becasue the amount can sometimes be a string, so I need to covert tot a number first
    amount = int(amount)
    return amount/100

def convert_float_to_int(amount):
        # Becasue the amount can sometimes be a string, so I need to covert tot a number first
    amount = float(amount)
    return int(amount*100)


            ### ### ### ### ### ### # TO-DO ---> Write comments ### ### ### ### ### ### ### ###

def get_days_of_a_month_in_calendar_as_abbr(year, month_as_int):
    
    #  monthrange() outputs the total number of days in a specific month
    # first_day : Is actually the correspondednt int day of the first day of month in calender, so for example if the first dat is Friday so int day will be '4', becasue Monday is '0'
    first_day, num_days = monthrange(year, month_as_int)
    
    # 'calender_days_in_month' is a list of dict, where each dict is {day_name:str day, day_num:Int day}
    # day_name[] : First of all notice that day_name[] is not a function !, it is an attribute, It takes int day as an index, then outputs the string name of day, where monday is '0' and tuseday is '1' ..etc
    calender_days_in_month_as_abbr = [{'day_name': day_name[(first_day + i) % 7]} for i in range(num_days)]

    return calender_days_in_month_as_abbr

def get_days_of_a_month_in_calendar_as_int(year, month_as_int):
    
    _, num_days = monthrange(year, month_as_int)
    
    calender_days_in_month_as_int = [{'day_num' : i + 1} for i in range(num_days)]
    
    return calender_days_in_month_as_int

def combine_int_days_and_abbr_days_in_one_list(calender_days_in_month_as_abbr, calender_days_in_month_as_int):
    
    calender_days_in_month = calender_days_in_month_as_abbr.copy()
    
    for i in range(len(calender_days_in_month)):
        calender_days_in_month[i].update(calender_days_in_month_as_int[i])
    
    return  calender_days_in_month
    
def get_calendar_days(year, month_as_int):
    
    calender_days_in_month_as_abbr = get_days_of_a_month_in_calendar_as_abbr(year, month_as_int)
    calender_days_in_month_as_int = get_days_of_a_month_in_calendar_as_int(year, month_as_int)
    calender_days_in_month = combine_int_days_and_abbr_days_in_one_list(calender_days_in_month_as_abbr, calender_days_in_month_as_int)
    
    return calender_days_in_month

def convert_num_months_to_abbr_months(months_as_num):
    
    months_as_abbr = []
    # Notice that we used 'month_as_num,' and not 'month_as_num' so there is ',' added !, and that to select the first element in the list of tuples ->"months_as_num [(11,), (9,), (8,), (6,)]"
    for month_as_num, in months_as_num:
        str_month = datetime(1, month_as_num, 1).strftime('%b')
        months_as_abbr.append(str_month)
        
    return months_as_abbr
                ### ### ### ### ### ### ### ### ### ### ### ### 
                
def validate_password(password):
    import re # regular expression
    if len(password) < 8:
        return ("Password should be at least 8 characters or longer")
    elif not re.search("[0-9]", password):
        return ("Password must contain at least one digit")
    elif not re.search("[A-Z]", password):
        return ("Password must contain at least one uppercase letter")
    elif not re.search("[@_!#$%&^*()<>?~+-/\{}:]",password):
        return ("password must contain at least one special charaster")
