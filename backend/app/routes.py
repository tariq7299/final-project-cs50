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
        
    # When user loads the page, it will populate the two <select> tags with calendar months of the current year, and calendar days of the current month
    if request.method == "GET":

        """
        I will actually view the months of current year only, because I didn't yet add the ability to enable users to choose a differnet year than the current one, to add expenses.
        So currently users can only choose a month and day from the current year.
        """
        current_year = datetime.now().year
        
        # I fetched current month, and selected it for user automtically, Because this route gets requested when user loads the page only
        current_month_int = datetime.now().month
        
        # Defines the months short names (abbreviations) in a list
        current_year_months_abbr = month_abbr[1:]
        
        # The current month name abbreviated (short name of month)
        current_month_abbr = month_abbr[current_month_int]

        current_day = datetime.now().day

        # This is a list of dicts, where each elemn¥ent cosists of two dictioneries the first contains day short name as "value", and the second dict contains the day as integer to be a "vale"  ---> [{'day_name': 'Thursday', 'day_num': 1}, {'day_name': 'Friday', 'day_num': 2}, ..... ] 
        calender_days_in_month = app.helpers.get_calendar_days(current_year, current_month_int)
        
        # THese are the expenses categories that will be sent to client, to choose one, so the expenses client made is added to that very categoty in db
        categories = ['Bills', 'Car', 'Clothes', 'Communication', 'Eating out', 'Entertainment', 'Food', 'Gifts', 'Health', 'House', 'Kids', 'Sports', 'Transport']
        
        response_object = {'status':'success', 'current_year_months': current_year_months_abbr, 'current_month':current_month_abbr, 'days':calender_days_in_month, 'current_day':current_day, 'categories':categories}

        return jsonify(response_object)
    
    # Now this gets requested whenever user chooses a month, so then it will populate the <select> tag of days, calendar days of that selected Month.
    elif request.method == "POST":
        
        post_data = request.get_json()
        
        # The selected month sent from client as the string short name of month, so we have to covert it to the Integer value, in order to be used later in code.
        selected_month_abbr   = post_data.get('selectedMonth')
        selected_month_num = datetime.strptime(selected_month_abbr, '%b').month
        
        current_year = datetime.now().year
        
        calender_days_in_selected_month = app.helpers.get_calendar_days(current_year, selected_month_num)
        
        response_object = {'status':'success', 'days':calender_days_in_selected_month}
         
        return jsonify(response_object)
    
# This route will get requested when user tries to submit his new expense
@appRoutes.route("/add_expenses", methods=["POST","GET"])
def add_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    if request.method == "POST":
        
        current_year = datetime.now().year
        
        post_data = request.get_json()
        selected_month_abbr   = post_data.get('selectedMonth')
        selected_month_num = datetime.strptime(selected_month_abbr, '%b').month
        selected_day  = post_data.get('selectedDay')
        submitted_amount_spent  = post_data.get('amountSpent')
        # Please rebuild the db mopdels, in order to maek the app doesn't accept empty category
        submitted_category  = post_data.get('category').strip()
       
        try:
            
            app.queries.expenses_queries.insert_new_expense_into_db(salah_id, current_year, selected_month_num, selected_day, submitted_amount_spent, submitted_category)
            
            submitted_amount_spent_as_egp_currency = app.helpers.egp(submitted_amount_spent)
            
            response_object = {'submitedAmountSpent': submitted_amount_spent_as_egp_currency, 'submitedCategory':submitted_category}
            
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
    
    if request.method == "GET":
        
        try: 
               
            # Definition of the most recent year
            
            # extract() is used to get the years from date object !, of the column 'date' of type 'db.date'
            # with_entities() It gets specific columns only
            years = app.queries.expenses_queries.select_years_contains_expenses(salah_id)

            most_recent_year = years[0]
            
            most_recent_month_of_expenses = app.queries.expenses_queries.select_most_recent_month(salah_id, most_recent_year)
            
            years_and_months = []
            for year in years:
                
                print('year', year)
                months = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == 2
                ).filter(
                    extract('year', UsersSpendings.date) == year
                ) .group_by(
                    extract('month', UsersSpendings.date)
                ).order_by(
                    extract('month', UsersSpendings.date).desc()
                ).all()
                
                months_list = []
                
                [ months_list.append(datetime(1, month, 1).strftime('%b')) for month, in months ]
                        
                years_and_months.append({'year': year, 'months': months_list, 'opened': False}) 
                           

            month_expenses = app.queries.expenses_queries.select_expenses_in_month(salah_id, most_recent_year, most_recent_month_of_expenses)
            
        
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(salah_id, most_recent_year, most_recent_month_of_expenses)
    
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(total_amount_of_month_expenses)

            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': spending.category} for spending in month_expenses]
                    
            response_object = { 'status': 'success', 'years_and_months': years_and_months, 'monthly_expenses': month_expenses_list,'total_amount_of_month_expenses': total_amount_of_month_expenses}
            
            # Return response object as JSON∆
            return jsonify(response_object)
        
        except Exception as e:

            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)

            return jsonify({'error_message': error_message}), 400

# @<bluebrint name>.route()
# USER CHOOSE MONTH IN SPENDING PAGE
@appRoutes.route("/fetch_selected_month_expenses", methods=["POST","GET"])
def fetch_selected_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    if request.method == "POST":
        
        try:    
            
            post_data = request.get_json()
            
            selected_year   = post_data.get('selectedYear')
            selected_month_abbr   = post_data.get('selectedMonth')
            selected_month_num = datetime.strptime(selected_month_abbr, '%b').month
            
            month_expenses = app.queries.expenses_queries.select_expenses_in_month(salah_id, selected_year, selected_month_num)
            
            # TO-DO ---> need to change some names here.
            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': spending.category} for spending in month_expenses]
            
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(salah_id, selected_year, selected_month_num)
            
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(total_amount_of_month_expenses)

            
            response_object = { 'status': 'success', 'monthly_expenses': month_expenses_list,'total_amount_of_month_expenses': total_amount_of_month_expenses}
            
            response_object['total_amount_of_month_expenses'] = total_amount_of_month_expenses

            response_object['monthly_expenses'] = month_expenses_list

            # Return response object as JSON
            return jsonify(response_object)
        
        except Exception as e:
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400