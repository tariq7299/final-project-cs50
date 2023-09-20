from flask import request, jsonify, Blueprint, redirect, render_template, session, url_for, flash
from app.models import db, Users, UsersSpendings, UsersWallets, Contacts, Relationships, Transactions
from datetime import datetime
from sqlalchemy import extract, func, and_
from calendar import month_abbr
import app.helpers
import app.queries.users_queries
import app.queries.expenses_queries

from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from app.helpers import login_required


appRoutes = Blueprint("routes", __name__)

@appRoutes.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@appRoutes.route("/register_user", methods=["POST","GET"])
def register():
    
    session.clear()
    
    if request.method == "POST":

        post_data = request.get_json()
        
        first_name = post_data.get('firstName')
        last_name = post_data.get('lastName')
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        password_confirm = post_data.get('passwordConfirm')
        
        # print('first_name', first_name)
        # print('last_name', last_name)
        # print('username', username)
        # print('email', email)
        # print('password', password)
        # print('password_confirm', password_confirm)
        
        hashed_password = generate_password_hash(password)
        # print('hashed_password', hashed_password)

        # If left any field empty
        if not username or not password or not password_confirm:
            error_message = 'Please fill in all fields !'
            return jsonify({'error_message': error_message}), 400

        # IF two passwords fields don't match
        if password != password_confirm:
            error_message = "Passwords don't match! Please try again."
            return jsonify({'error_message': error_message}), 400
        
        # Validate the password if it containes especial characters and should 8 characters long
        # if helpers.validate_password(password):
        #     flash_message = helpers.validate_password(password)
        #     flash(flash_message)
        #     return redirect(url_for('register'))

        # Checks if username already exists in database
        db_username = db.session.query(Users.username).filter(Users.username==username).scalar()
        
        print('db_username', db_username)
        
        if db_username:
            error_message = "Username already exists! Please choose a new one."
            return jsonify({'error_message': error_message}), 400
        
        try: 
            
            new_user = Users(first_name=first_name, last_name=last_name, username=username, email=email, hash=hashed_password)
            
            db.session.add(new_user)
            
            user_id = db.session.query(Users.user_id).filter(Users.username==username).scalar()
            
            print('user_id', user_id)
            
            db.session.commit()
            
            # success="true" get added as a query in the url of login.html
            # this will activate alert() function in JS
            response_object = {'success': True}
             
            return jsonify(response_object)
        
        except Exception as e:
            db.session.rollback()
            
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            
            db.session.close()

@appRoutes.route("/login", methods=["POST"])
def login():
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        post_data = request.get_json()
        
        username = post_data.get('username')
        password = post_data.get('password')

        # Ensure username was submitted
        if not username:
            error_message = "must provide username"
            return jsonify({'error_message': error_message}), 400

        # Ensure password was submitted
        elif not password:
            error_message = "must provide password"
            return jsonify({'error_message': error_message}), 400
        

        # Query database for username
        user_info = db.session.query(Users.user_id, Users.username, Users.hash).filter(Users.username==username).all()
        
        print('user_info', user_info)
        
        for user_tuple in user_info:
            print('user_tuple', user_tuple)
            user_id = user_tuple[0]
            db_username = user_tuple[1]
            hash_value = user_tuple[2]
            
        # Ensure username exists and password is correct
        if not db_username or not check_password_hash(hash_value, password):
            error_message = "invalid username and/or password"
            return jsonify({'error_message': error_message}), 400

        # Remember which user has logged in
        session["user_id"] = user_id

        response_object = {'success': True}
             
        return jsonify(response_object)

@appRoutes.route("/logout", methods=["GET"])
def logout():
    
    session.clear()
    
    response_object = {'success': True}
    
    return jsonify(response_object)
    
    
@appRoutes.route("/user_wallet", methods=["POST","GET"])
@login_required
def user_wallet():
    
    current_user_id = session.get('user_id')
    print('user_id_wallet', current_user_id)
    
    # Replace this user id from by the one foumd in session['user_id']
    # current_user_id = session["user_id"]
    # current_user_id = session["user_id"]
    
    # print('current_user_id', current_user_id)
    
    # IF we GET this route, to we need to sent to frontend the months and days of the current year
    if request.method == "GET":
        try:
            
            total_net_balance = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==current_user_id).scalar()
            
            total_net_balance = total_net_balance or 0
            
            # print('total_net_balance1', total_net_balance)
               
            total_net_balance = app.helpers.egp(app.helpers.convert_int_to_float(total_net_balance)) 
            
            # print('total_net_balance2', total_net_balance)
            
            debt = 0
            credit = 0

            net_balance_per_contact = db.session.query(func.sum(Transactions.amount).label('contact_net_balance')).filter(Transactions.user_id==current_user_id).group_by(Transactions.contact_id).all()
            
            net_balance_per_contact = net_balance_per_contact or []
            
            # print('net_balance_per_contact', net_balance_per_contact)
            
            for net_balance, in net_balance_per_contact:
                if net_balance > 0:
                    credit += net_balance
                else:
                    debt += net_balance
            
            debt =  app.helpers.egp(app.helpers.convert_int_to_float(debt))
            credit =  app.helpers.egp(app.helpers.convert_int_to_float(credit))
            
            # print('debt', debt)
            # print('credit', credit)
            
            wallet = {'netBalance': total_net_balance, 'credit': credit, 'debt': debt}
            
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
@login_required
def get_calendar():
        
    # When user loads the page, it will populate the two <select> tags with calendar months of the current year, and calendar days of the current month
    if request.method == "GET":

        
        # THese are the expenses categories that will be sent to client, to choose one, so the expenses client made is added to that very categoty in db
        categories = ['Bills', 'Car', 'Clothes', 'Communication', 'Eating out', 'Entertainment', 'Food', 'Gifts', 'Health', 'House', 'Kids', 'Sports', 'Transport']
        
        response_object = {'status':'success', 'categories':categories}

        return jsonify(response_object)
    
# This route will get requested when user tries to submit his new expense
@appRoutes.route("/add_expenses", methods=["POST","GET"])
@login_required
def add_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session.get('user_id')
    print('current_user_id_add_expenses', current_user_id)
    
    if request.method == "POST":
        
        
        post_data = request.get_json()
        selected_year   = post_data.get('selectedYear')
        selected_month_num   = post_data.get('selectedMonth')
        selected_day  = post_data.get('selectedDay')
        submitted_amount_spent  = post_data.get('amountSpent')
        # Please rebuild the db mopdels, in order to maek the app doesn't accept empty category
        submitted_category  = post_data.get('category').strip()
        expense_note = post_data.get('expenseNote')
       
        if expense_note == '' : expense_note = None
       
        # print('selected_year', selected_year)
        # print('selected_month_num', selected_month_num)
        # print('selected_day', selected_day)
        # print('submitted_amount_spent', submitted_category)
        # print('expense_note', expense_note)
        
        try:
            
            app.queries.expenses_queries.insert_new_expense_into_db(current_user_id, selected_year, selected_month_num, selected_day, submitted_amount_spent, submitted_category, expense_note)
            
            submitted_amount_spent_as_egp_currency = app.helpers.egp(submitted_amount_spent)
            
            response_object = {'status': 'success', 'submitedAmountSpent': submitted_amount_spent_as_egp_currency, 'submitedCategory':submitted_category}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
            
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            
            db.session.close()

# USER LOADS SPENDING PAGE
@appRoutes.route("/load_recent_month_expenses", methods=["POST","GET"])
@login_required
def load_recent_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session.get('user_id')
    
    print('user_id_load', current_user_id)
    
    if request.method == "GET":
        
        try: 
               
            # Definition of the most recent year
            
            # extract() is used to get the years from date object !, of the column 'date' of type 'db.date'
            # with_entities() It gets specific columns only
            years = app.queries.expenses_queries.select_years_contains_expenses(current_user_id)
            # print('years', years)
            # This would mean that there is no expenses found in db
            if not years:
                response_object = { 'status': 'success', 'noExpensesFound': True}
                return jsonify(response_object)
            
            
            most_recent_year = years[0]
            # print('most_recent_year', most_recent_year)
            
            most_recent_month_of_expenses = app.queries.expenses_queries.select_most_recent_month(current_user_id, most_recent_year)
            # print('most_recent_month_of_expenses', most_recent_month_of_expenses)
            
            years_and_months = []
            for year in years:
                
                months = UsersSpendings.query.with_entities(
                    extract('month', UsersSpendings.date)
                ).filter(
                    UsersSpendings.user_id == current_user_id
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
                           
            # print('months_list', months_list)
            # print('years_and_months', years_and_months)

            month_expenses = app.queries.expenses_queries.select_expenses_in_month(current_user_id, most_recent_year, most_recent_month_of_expenses)
            
            # print('month_expenses', month_expenses)
        
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(current_user_id, most_recent_year, most_recent_month_of_expenses)
    
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(app.helpers.convert_int_to_float(total_amount_of_month_expenses))

            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': spending.category, 'note': spending.note} for spending in month_expenses]
                    
            response_object = { 'status': 'success', 'years_and_months': years_and_months, 'monthly_expenses': month_expenses_list,'total_amount_of_month_expenses': total_amount_of_month_expenses}
            
            # Return response object as JSON∆
            return jsonify(response_object)
        
        except Exception as e:

            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)

            return jsonify({'error_message': error_message}), 400

# @<bluebrint name>.route()
# USER CHOOSE MONTH IN SPENDING PAGE
@appRoutes.route("/fetch_selected_month_expenses", methods=["POST","GET"])
@login_required
def fetch_selected_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session["user_id"]
    
    if request.method == "POST":
        
        try:    
            
            post_data = request.get_json()
            
            selected_year   = post_data.get('selectedYear')
            selected_month_abbr   = post_data.get('selectedMonth')
            selected_month_num = datetime.strptime(selected_month_abbr, '%b').month
            
            month_expenses = app.queries.expenses_queries.select_expenses_in_month(current_user_id, selected_year, selected_month_num)
            
            # TO-DO ---> need to change some names here.
            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': spending.category, 'note': spending.note} for spending in month_expenses]
            
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(current_user_id, selected_year, selected_month_num)
            
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(app.helpers.convert_int_to_float(total_amount_of_month_expenses))

            
            response_object = { 'status': 'success', 'monthly_expenses': month_expenses_list,'total_amount_of_month_expenses': total_amount_of_month_expenses}
            
            # response_object['total_amount_of_month_expenses'] = total_amount_of_month_expenses

            # response_object['monthly_expenses'] = month_expenses_list

            # Return response object as JSON
            return jsonify(response_object)
        
        except Exception as e:
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400

@appRoutes.route("/net_balance", methods=["POST","GET"])
@login_required
def load_net_balance():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session["user_id"]
    
    if request.method == "GET":
        try:
            
            net_balance = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==current_user_id).scalar()
            
            net_balance = app.helpers.egp(app.helpers.convert_int_to_float(net_balance))
            
            # We have to put "wallet" into an abject to jsonify() it later, so we can send it to the client
            response_object = { 'status': 'success', 'net_balance': net_balance }
            
            return jsonify(response_object)
        
        # If any problem arises then return error message to the client
        except Exception as e:
            
            # the Excepting hta has risen "str(e)" will included in the error message sent to user
            error_message = 'An error occurred while fetching net balance! Error message: ' + str(e)
            
            response_object = {'error_message': error_message}
            
            return jsonify(response_object), 400
            
@appRoutes.route("/people", methods=["POST","GET"])
@login_required
def load_people():
    
    current_user_id = session.get('user_id')
    
    if request.method == "GET":
        try:
                         
            #   With utlizing the 'lazy' and 'realatioship' technique/feature (this defined in the db model itself)
            transactions = db.session.query(Transactions, func.sum(Transactions.amount).label('contact_net_balance')).filter(Transactions.user_id==current_user_id).group_by(Transactions.contact_id).all()
            
            # for transaction in transactions:
                # print('transaction.contact_name__2', transaction[0].contact.name)
            #     print('transaction.contact_phone', transaction[0].user.name)
            #     print('transaction_amount', transaction.contact_net_balance)
            
            transactions_list = [{'contact_name': transaction[0].contact.name, 'contact_phone': transaction[0].contact.phone, 'transations_net_balance': app.helpers.convert_int_to_float(transaction.contact_net_balance)} for transaction in transactions] 
            
            # We have to put "wallet" into an abject to jsonify() it later, so we can send it to the client
            response_object = { 'status': 'success', 'transactions': transactions_list }
            
            # print('transactions_list', transactions_list)
            
            return jsonify(response_object)
        
     # If any problem arises then return error message to the client
        except Exception as e:
            
            # the Excepting hta has risen "str(e)" will included in the error message sent to user
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            
            response_object = {'error_message': error_message}
            
            return jsonify(response_object), 400
        
    # this user presses on any Contact to see that contact history
    if request.method == "POST":
        try:    
            
            post_data = request.get_json()
            
            contact_phone   = post_data.get('contactPhone')
            
            transactions = db.session.query(Transactions).filter(and_(Transactions.user_id==current_user_id), (Contacts.phone==contact_phone)).order_by(Transactions.date.desc()).join(Contacts)
    
            transactions_list = [{'id': transaction.id, 'date': transaction.date.strftime("%a %d/%m/%Y"), 'amount': app.helpers.convert_int_to_float(transaction.amount), 'note': transaction.note} for transaction in transactions]
            
            # print('transactions_list', transactions_list)
            
            response_object = { 'status': 'success', 'transactions': transactions_list}
            
            # Return response object as JSON
            return jsonify(response_object)
        
        except Exception as e:
            error_message = 'An error occurred while fetching expenses! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
@appRoutes.route("/new-contact", methods=["POST","GET"])
@login_required
def add_new_contact():
    
    current_user_id = session.get('user_id')
     
    if request. method == 'POST':
        try:
            post_data = request.get_json()  
            
            new_contact_name = post_data.get('contactName').strip()
            
            new_contact_phone = post_data.get('contactPhone').strip()   
            
            new_contact = Contacts(name=new_contact_name, phone=new_contact_phone)
            db.session.add(new_contact)
            db.session.commit()
            
            
            # Try a new way to get the 'user_id', like by joininng the two tables toghether then extracting the user_id where name is 'Mohamed' --for example
            new_relationship = Relationships(user_id=current_user_id, contact_id=new_contact.id)
            db.session.add(new_relationship)
            db.session.commit()
            
            response_object = {'status': 'success', 'newContactName': new_contact_name, 'newContactPhone':new_contact_phone}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
                
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            db.session.close()
            
@appRoutes.route("/new-transactions", methods=["POST","GET"])
@login_required
def new_transactions():
     
    current_user_id = session.get('user_id')
    print('current_user_id', current_user_id)
    
    if request.method == "GET":

        contacts = db.session.query(Contacts).filter(Relationships.user_id==current_user_id).join(Relationships, Relationships.contact_id == Contacts.id).all()
                
        contacts_list = [{'contact_phone': contact.phone, 'contact_name': contact.name, } for contact in contacts]
                
        contacts_names = []
        
        [contacts_names.append(contact.name) for contact in contacts]
        
        print(contacts_list)
        # print('contacts_names', contacts_names)
        
        response_object = {'status':'success', 'contacts': contacts_list}

        return jsonify(response_object)
    
    elif request.method == "POST":
        
        # Needs validation ! (Empty values, Incorrect type, IF note provided as an empty string then assign it as None, to make db assing it a default value)
        post_data = request.get_json()
        selected_year   = post_data.get('selectedYear')
        selected_month_num   = post_data.get('selectedMonth')
        selected_day  = post_data.get('selectedDay')
        submittedAmount  = post_data.get('submittedAmount')
        # Please rebuild the db mopdels, in order to maek the app doesn't accept empty category
        new_contact_phone  = post_data.get('newContactPhone')
        transaction_note = post_data.get('transactionNote')
        
        if transaction_note == '' : transaction_note = None
        
        

        try:
            
            submitted_integer_amount = app.helpers.convert_float_to_int(submittedAmount)

            new_contact_id = db.session.query(Contacts.id).filter(Contacts.phone==new_contact_phone).scalar()
            
            new_transactions = Transactions(amount=submitted_integer_amount, date=datetime(selected_year, selected_month_num, selected_day), user_id=current_user_id, contact_id=new_contact_id, note=transaction_note)
            
            db.session.add(new_transactions)
            
            db.session.commit()
            
            submitted_amount_as_egp_currency = app.helpers.egp(submittedAmount)
            
            new_contact_name = db.session.query(Contacts.name).filter(Contacts.phone==new_contact_phone).scalar()
            
            response_object = {'submittedAmount': submitted_amount_as_egp_currency, 'submittedContactName':new_contact_name}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
            
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            
            db.session.close()
