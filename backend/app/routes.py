from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings, UsersWallets
from datetime import datetime
from sqlalchemy import extract, func
from calendar import monthrange, day_name, month_abbr
import app.helpers
import app.queries.users_queries
import app.queries.expenses_queries

appRoutes = Blueprint("routes", __name__)



@appRoutes.route("/user_wallet", methods=["POST","GET"])
def user_wallet():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    # IF we GET this route, to we need to sent to frontend the months and days of the current year
    if request.method == "GET":
        try:
            
            # 'wallet' contains user wallet info (balance, debt, credit)
            wallet = app.queries.users_queries.get_user_wallet(salah_id)
            
            # We have to put "wallet" into an abject to jsonify() it later, so we can send it to the client
            response_object = { 'status': 'success', 'wallet': wallet }
            
            return jsonify(response_object)
        
        # If any problem arises then return error message to the client
        except Exception as e:
            
            # the Excepting hta has risen "str(e)" will included in the error message sent to user
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            
            response_object = {'error_message': error_message}
            
            return jsonify(response_object), 400

@appRoutes.route("/get_calendar", methods=["POST","GET"])
def get_calendar():
    
    current_year = datetime.now().year
    
    # When user loads the page, it will populate the two <select> tags with calendar months of the current year, and calendar days of the current month
    if request.method == "GET":
        
        current_month_int = datetime.now().month

        # Get the abbreviated list of month names
        current_year_months_abbr = month_abbr[1:]

        current_month_abbr = month_abbr[current_month_int]

        current_day = datetime.now().day

        #  monthrange() outputs the total number of days in a specific month
        # first_day : Is actually the correspondednt int day of the first day of month in calender, so for example if the first dat is Friday so int day will be '4', becasue Monday is '0'
        first_day, num_days = monthrange(current_year, current_month_int)
        
        # 'calender_days_in_month' is a list of tuples, where each tuple is (str day, Int day)
        # day_name[] : First of all notice that day_name[] is not a function !, it is an attribute, It takes int day as an index, then outputs the string name of day, where monday is '0' and tuseday is '1' ..etc
        calender_days_in_month = [{'day_name': day_name[(first_day + i) % 7],  'day_num' : i + 1} for i in range(num_days)]
        
        # THese are the expenses categories that will be sent to client, to choose one, so the expenses client made is added to that very categoty in db
        categories = ['Bills', 'Car', 'Clothes', 'Communication', 'Eating out', 'Entertainment', 'Food', 'Gifts', 'Health', 'House', 'Kids', 'Sports', 'Transport']
        
        response_object = {'status':'success', 'current_year_months': current_year_months_abbr, 'current_month':current_month_abbr, 'days':calender_days_in_month, 'current_day':current_day, 'categories':categories}

        return jsonify(response_object)
    
    elif request.method == "POST":
        
        post_data = request.get_json()
        selected_month_str   = post_data.get('selectedMonth')
        selected_month_int = datetime.strptime(selected_month_str, '%b').month
        
        first_day, num_days = monthrange(current_year, selected_month_int)

        calender_days_in_selected_month = [{'day_name': day_name[(first_day + i) % 7],  'day_num' : i + 1} for i in range(num_days)]

        response_object = {'status':'success', 'days':calender_days_in_selected_month}
         
        return jsonify(response_object)
    
    
@appRoutes.route("/add_expenses", methods=["POST","GET"])
def add_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    if request.method == "POST":
        
        current_year = datetime.now().year
        
        post_data = request.get_json()
        selected_month_str   = post_data.get('selectedMonth')
        selected_month_int = datetime.strptime(selected_month_str, '%b').month
        selected_day  = post_data.get('selectedDay')
        submitted_amount_spent  = post_data.get('amountSpent')
        submitted_category  = post_data.get('category')
                
        new_expense = UsersSpendings(user_id=salah_id, date=datetime(current_year, selected_month_int, selected_day).date(), amount_spent=submitted_amount_spent, category=submitted_category)
       
        try:
            db.session.add(new_expense)
            response_object = {'submitedAmountSpent': submitted_amount_spent, 'submitedCategory':submitted_category}
            
            # You cannot rollback() if you executed commit()
            db.session.commit()
            return jsonify(response_object)
        except Exception as e:
            db.session.rollback()
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        finally:
            db.session.close()


# USER LOADS SPENDING PAGE
@appRoutes.route("/load_recent_month_expenses", methods=["POST","GET"])
def load_recent_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    response_object = {'status':'success'}
    if request.method == "GET":
        
        # Definition of the most recent year
        
        # extract() is used to get the years from date object !, of the column 'date' of type 'db.date'
        # with_entities() It gets specific columns only
        years = UsersSpendings.query.with_entities(
                extract('year', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == salah_id
            ).group_by(
                extract('year', UsersSpendings.date)
            ).order_by(
                extract('year', UsersSpendings.date).desc()
            ).all()

        most_recent_year = years[0][0]
        
        most_recent_month_list = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == salah_id
                ).filter(
                    extract('year', UsersSpendings.date) == most_recent_year
                ) .group_by(
                    extract('month', UsersSpendings.date)
                ).order_by(
                    extract('month', UsersSpendings.date).desc()
                ).first()
                
        most_recent_month = most_recent_month_list[0]
        
        months = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == salah_id
                ).filter(
                    extract('year', UsersSpendings.date) == most_recent_year
                ) .group_by(
                    extract('month', UsersSpendings.date)
                ).order_by(
                    extract('month', UsersSpendings.date).desc()
                ).all()

        str_month_list = []
        
        for int_month, in months:
            str_month = datetime(1, int_month, 1).strftime('%b')
            str_month_list.append(str_month)
        
        
        month_spendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == most_recent_year).filter(extract('month', UsersSpendings.date) == most_recent_month).order_by(UsersSpendings.date.desc()).all()

        total_monthly_expenses = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == most_recent_year).filter(extract('month', UsersSpendings.date) == most_recent_month).scalar()
        
        month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'category': spending.category} for spending in month_spendings]
        
        # print(len(month_spendings_list))        
        # print(len(total_daily_spendings_list))        
        # for i in range(len(month_spendings_list)):
        #     month_spendings_list[i].update(total_daily_spendings_list[i])
        
        
        # [print(spending) for spending in month_spendings_list]
        
        # Add years data to response object
        # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
        response_object['years'] = [year[0] for year in years]
        # Add years data to response object
        # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
        response_object['months'] = str_month_list
        
        # For tests
        # [print('spending', spending) for spending in month_spendings]
        
        response_object['monthly_expenses'] = month_spendings_list
        
        response_object['total_monthly_expenses'] = total_monthly_expenses
        
        
        # response_object['total_daily_spendings'] = total_daily_spendings_list
        
        # Return response object as JSON∆
        return jsonify(response_object)
    
# @<bluebrint name>.route()
# USER CHOOSE YEAR IN SPENDING PAGE
@appRoutes.route("/fetch_months_and_recent_month_expenses", methods=["POST","GET"])
def fetch_months_and_recent_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    response_object = {'status':'success'}
    
    if request.method == "POST":
            
        post_data = request.get_json()
        
        selected_year   = post_data.get('selectedYear')
        
        

        most_recent_month_list = UsersSpendings.query.with_entities(
                extract('month', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == salah_id
            ).filter(
                extract('year', UsersSpendings.date) == selected_year
            ) .group_by(
                extract('month', UsersSpendings.date)
            ).order_by(
                extract('month', UsersSpendings.date).desc()
            ).first()
            
        most_recent_month = most_recent_month_list[0]
        
        months = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == salah_id
                ).filter(
                    extract('year', UsersSpendings.date) == selected_year
                ) .group_by(
                    extract('month', UsersSpendings.date)
                ).order_by(
                    extract('month', UsersSpendings.date).desc()
                ).all()
        str_month_list = []
        
        for int_month, in months:
            str_month = datetime(1, int_month, 1).strftime('%b')
            str_month_list.append(str_month)
            
                    #  monthrange() outputs the total number of days in a specific month

        month_spendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).order_by(UsersSpendings.date.desc()).all()
    
        month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'category': spending.category} for spending in month_spendings]
        
        total_monthly_expenses = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).scalar()

        # total_daily_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).filter().group_by(extract('day', UsersSpendings.date)).order_by(extract('month', UsersSpendings.date).desc()).all()

        # total_daily_spendings_list = [{'total_daily_spending': row[0]} for row in total_daily_spendings]
        
        response_object['months'] = str_month_list
        
        response_object['total_monthly_expenses'] = total_monthly_expenses
        


        
        # response_object['total_daily_spendings'] = total_daily_spendings_list

        response_object['monthly_expenses'] = month_spendings_list

        # Return response object as JSON
        return jsonify(response_object)
    
# @<bluebrint name>.route()
# USER CHOOSE MONTH IN SPENDING PAGE
@appRoutes.route("/fetch_selected_month_expenses", methods=["POST","GET"])
def fetch_selected_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    response_object = {'status':'success'}
    
    if request.method == "POST":
        
        try:    
            post_data = request.get_json()
            
            selected_year   = post_data.get('selectedYear')
            selected_month_str   = post_data.get('selectedMonth')
            selected_month_int = datetime.strptime(selected_month_str, '%b').month
            
            month_spendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == selected_month_int).order_by(UsersSpendings.date.desc()).all()
            
        
            month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'category': spending.category} for spending in month_spendings]
            
            total_monthly_expenses = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == selected_month_int).scalar()
                    
            response_object['total_monthly_expenses'] = total_monthly_expenses

            response_object['monthly_expenses'] = month_spendings_list

            # Return response object as JSON
            return jsonify(response_object)
        
        except Exception as e:
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# @appRoutes.route("/fetchMonths", methods=["POST","GET"])
# def fetchMonths():
#     response_object = {'status':'success'}
#     if request.method == "POST":
        
#         post_data = request.get_json()
#         selected_year   = post_data.get('selectedYear')
        
#         # Replace this user id from by the one foumd in session['user_id']
#         salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id

#         # extract() is used to get the years from date object !, of the column 'date' of type 'db.date'
#         # with_entities() It gets specific columns only
#         months = UsersSpendings.query.with_entities(
#                 extract('month', UsersSpendings.date)
#             ).filter(
#                 UsersSpendings.user_id == salah_id
#             ).filter(
#                 extract('year', UsersSpendings.date) == selected_year
#             ) .group_by(
#                 extract('month', UsersSpendings.date)
#             ).order_by(
#                 extract('month', UsersSpendings.date).desc()
#             ).all()

#         str_month_list = []
#         for int_month, in months:
#             str_month = datetime(1, int_month, 1).strftime('%b')
#             str_month_list.append(str_month)
            
#         # Add years data to response object
#         # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
#         print(selected_year)
#         response_object['months'] = str_month_list
        
#     # Return response object as JSON
#     return jsonify(response_object)
        
