from flask import request, jsonify, Blueprint, redirect, render_template, session, url_for, flash, make_response
from app.models import db, Users, UsersSpendings, UsersWallets, Contacts, Relationships, Transactions, Categories, UserCategory
from datetime import datetime
from sqlalchemy import extract, func, and_
from calendar import month_abbr
import app.helpers
import app.queries.users_queries
import app.queries.expenses_queries

from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from app.helpers import login_required
from uuid import uuid4

appRoutes = Blueprint("routes", __name__)

@appRoutes.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@appRoutes.route("/is-authenticated", methods=["GET"])
def is_authenticated():
    return jsonify({'isLogged': True}) if bool(session.get('user_id')) else jsonify({'isLogged': False})

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
        
        hashed_password = generate_password_hash(password)

        # If left any field empty
        if not username or not password or not password_confirm:
            error_message = 'Please fill in all fields !'
            return jsonify({'error_message': error_message}), 400

        # IF two passwords fields don't match
        if password != password_confirm:
            error_message = "Passwords don't match! Please try again."
            return jsonify({'error_message': error_message}), 400
        
        # Checks if username already exists in database
        db_username = db.session.query(Users.username).filter(Users.username==username).scalar()
        
        db_email = db.session.query(Users.email).filter(Users.email==email).scalar()
                
        if bool(db_username) or bool(db_email):
            error_message = "Username/Email already exists! Please choose a new one."
            return jsonify({'error_message': error_message}), 400
        
        if app.helpers.validate_password(password):
            error_message = app.helpers.validate_password(password)
            return jsonify({'error_message': error_message}), 400
        
        try: 
            
            new_user = Users(first_name=first_name, last_name=last_name, username=username, email=email, hash=hashed_password)
            
            db.session.add(new_user)
            
            new_user_id = db.session.query(Users.user_id).filter(Users.username==username).scalar()
            
            db.session.commit()
            
            for default_category_id in range(1, 14, 1):
                new_user_category = UserCategory(user_id=new_user_id, category_id=default_category_id)
                
                db.session.add(new_user_category)
            
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
        user_info_tuple = db.session.query(Users.user_id, Users.username, Users.hash).filter(Users.username==username).first()
        
        if not user_info_tuple:
            error_message = "No account Asociated with that user name, please register first !"
            return jsonify({'error_message': error_message}), 400
        
        user_id = user_info_tuple[0]
        db_username = user_info_tuple[1]
        hash_value = user_info_tuple[2]
            
        # Ensure username exists and password is correct
        if not db_username or not check_password_hash(hash_value, password):
            error_message = "invalid username and/or password"
            return jsonify({'error_message': error_message}), 400

        # Generate a CSRF token (you may use a library or generate it securely)
        csrf_token = uuid4()
        # Remember which user has logged in
        session["user_id"] = user_id

        session['csrf_token'] = str(csrf_token)
        
        print("session['csrf_token']", session['csrf_token'])
        # Set the CSRF token as an HttpOnly cookie
        response = jsonify({'success': True, 'csrf_token': csrf_token})
        
        response.set_cookie('csrfToken', value=str(csrf_token), httponly=True)
        return response

             

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
        
    # IF we GET this route, to we need to sent to frontend the months and days of the current year
    if request.method == "GET":
        try:
            
            total_net_balance = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==current_user_id).scalar()
            
            total_net_balance = total_net_balance or 0
            
            total_net_balance = app.helpers.egp(app.helpers.convert_int_to_float(total_net_balance)) 
            
            debt = 0
            credit = 0

            net_balance_per_contact = db.session.query(func.sum(Transactions.amount).label('contact_net_balance')).filter(Transactions.user_id==current_user_id).group_by(Transactions.contact_id).all()
            
            net_balance_per_contact = net_balance_per_contact or []
            
            for net_balance, in net_balance_per_contact:
                if net_balance > 0:
                    credit += net_balance
                else:
                    debt += net_balance
            
            debt =  app.helpers.egp(app.helpers.convert_int_to_float(debt))
            credit =  app.helpers.egp(app.helpers.convert_int_to_float(credit))
            
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
    
    current_user_id = session.get('user_id')
        
    # When user loads the page, it will populate the two <select> tags with calendar months of the current year, and calendar days of the current month
    if request.method == "GET":

        user_categories = db.session.query(Categories).filter(UserCategory.user_id==current_user_id).join(UserCategory).all()
        
        user_categories_list = [{'category_id': user_category.id, 'category_name': user_category.name} for user_category in user_categories]
        
        response_object = {'status':'success', 'categories':user_categories_list}
        
        return jsonify(response_object)
        
# This route will get requested when user tries to submit his new expense
@appRoutes.route("/add_expenses", methods=["POST","GET"])
@login_required
def add_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session.get('user_id')
    
    if request.method == "POST":
        
        post_data = request.get_json()
        
        
        try: 
            selected_year   = post_data.get('selectedYear')
            selected_month_num   = post_data.get('selectedMonth')
            selected_day  = post_data.get('selectedDay')
            submitted_amount_spent  = float(post_data.get('amountSpent'))
            submitted_category_id  = post_data.get('categoryId')
            expense_note = post_data.get('expenseNote')
            
            # Please rebuild the db mopdels, in order to maek the app doesn't accept empty category
            
            if session.get('csrf_token') != request.cookies.get('csrfToken'):
                error_message = 'Unathorised access'
                return jsonify({'error_message': error_message}), 400
            
            if not all([selected_year, selected_month_num, selected_day, submitted_amount_spent, submitted_category_id]):
                    error_message = 'All fields are required'
                    return jsonify({'error_message': error_message}), 400
                
            datetime(int(selected_year), int(selected_month_num), int(selected_day))
                
            if submitted_amount_spent <= 0:
                error_message = 'Amount spent must be a positive number'
                return jsonify({'error_message': error_message}), 400
                
            if not bool(expense_note): 
                expense_note = None
            elif bool(expense_note): 
                expense_note = expense_note.strip()
                
        except Exception as e:
            error_message = 'Please Enter a valid Data'
            return jsonify({'error_message': error_message}), 400
        

       
        try:
            
            app.queries.expenses_queries.insert_new_expense_into_db(current_user_id, selected_year, selected_month_num, selected_day, submitted_amount_spent, submitted_category_id, expense_note)
            
            submitted_amount_spent_as_egp_currency = app.helpers.egp(submitted_amount_spent)
            
            submitted_category_name = db.session.query(Categories.name).filter(Categories.id==submitted_category_id).scalar()
            
            response_object = {'status': 'success', 'submitedAmountSpent': submitted_amount_spent_as_egp_currency, 'submitedCategoryName':submitted_category_name}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
            
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            
            db.session.close()

@appRoutes.route("/new-category", methods=["POST","GET"])
@login_required
def add_new_category():
    
    current_user_id = session.get('user_id')
    
    if request.method == 'POST':
        
        try: 
            post_data = request.get_json()  
            
            try: 
                
                new_category_name = post_data.get('categoryName').strip()
            
                if not bool(new_category_name):
                        error_message = 'All fields are required'
                        return jsonify({'error_message': error_message}), 400
                
                if session.get('csrf_token') != request.cookies.get('csrfToken'):
                    error_message = 'Unathorised access'
                    return jsonify({'error_message': error_message}), 400
            
            except Exception as e:
                error_message = 'Please Enter a valid Data'
                return jsonify({'error_message': error_message}), 400
            
            category_id = db.session.query(Categories.id).filter(Categories.name==new_category_name).scalar()
            
            if not bool(category_id):
                new_category = Categories(name=new_category_name)
                db.session.add(new_category)
                db.session.commit()
                category_id = new_category.id
                
            db_user_category = db.session.query(UserCategory).filter(UserCategory.user_id==current_user_id, UserCategory.category_id==category_id).all()          
                  
            
            if bool(db_user_category):
                error_message = "Category already exists!."
                return jsonify({'error_message': error_message}), 400
            
            new_user_category = UserCategory(user_id=current_user_id, category_id=category_id)
            db.session.add(new_user_category)
            db.session.commit()

            response_object = {'status': 'success', 'newCategoryName': new_category_name}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
                
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
    
# USER LOADS SPENDING PAGE
@appRoutes.route("/load_recent_month_expenses", methods=["POST","GET"])
@login_required
def load_recent_month_expenses():
    
    # Replace this user id from by the one foumd in session['user_id']
    current_user_id = session.get('user_id')
    
    print('user_id_load', current_user_id)
    
    if request.method == "GET":
        
        try: 
            
            years = app.queries.expenses_queries.select_years_contains_expenses(current_user_id)
            
            # This would mean that there is no expenses found in db
            if not years:
                response_object = { 'status': 'success', 'noExpensesFound': True}
                return jsonify(response_object)
            
            most_recent_year = years[0]
            
            most_recent_month_of_expenses = app.queries.expenses_queries.select_most_recent_month(current_user_id, most_recent_year)
            
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
                           
            month_expenses = app.queries.expenses_queries.select_expenses_in_month(current_user_id, most_recent_year, most_recent_month_of_expenses)
                    
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(current_user_id, most_recent_year, most_recent_month_of_expenses)
    
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(app.helpers.convert_int_to_float(total_amount_of_month_expenses))

            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': category_name, 'note': spending.note} for spending, category_name in month_expenses]
                    
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
            month_expenses_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(spending.amount_spent), 'category': category_name, 'note': spending.note} for spending, category_name in month_expenses]
            
            total_amount_of_month_expenses = app.queries.expenses_queries.extract_total_amount_of_month_expenses(current_user_id, selected_year, selected_month_num)
            
            # Formatig the total amount spent as a currency 
            total_amount_of_month_expenses = app.helpers.egp(app.helpers.convert_int_to_float(total_amount_of_month_expenses))

            response_object = { 'status': 'success', 'monthly_expenses': month_expenses_list,'total_amount_of_month_expenses': total_amount_of_month_expenses}
            
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
            
            transactions_list = [{'contact_name': transaction[0].contact.name, 'contact_phone': transaction[0].contact.phone, 'transations_net_balance': app.helpers.convert_int_to_float(transaction.contact_net_balance)} for transaction in transactions] 
            
            # We have to put "wallet" into an abject to jsonify() it later, so we can send it to the client
            response_object = { 'status': 'success', 'transactions': transactions_list }
                        
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
     
    if request.method == 'POST':
        
        try:
            post_data = request.get_json()  
            
            try: 
                
                new_contact_name = post_data.get('contactName').strip()
            
                new_contact_phone = post_data.get('contactPhone')
                
                if not all([new_contact_name, new_contact_phone]):
                        error_message = 'All fields are required'
                        return jsonify({'error_message': error_message}), 400
                
                if session.get('csrf_token') != request.cookies.get('csrfToken'):
                    error_message = 'Unathorised access'
                    return jsonify({'error_message': error_message}), 400
            
            except Exception as e:
                print(e)
                error_message = 'Please Enter a valid Data'
                return jsonify({'error_message': error_message}), 400

            contact_id = db.session.query(Contacts.id).filter(Contacts.phone==new_contact_phone).scalar()
            
            if not bool(contact_id):
                new_contact = Contacts(name=new_contact_name, phone=new_contact_phone)
                db.session.add(new_contact)
                db.session.commit()
                contact_id = new_contact.id
                
            db_user_relationship = db.session.query(Relationships).filter(Relationships.user_id==current_user_id, Relationships.contact_id==contact_id).all()    
            
            if bool(db_user_relationship):
                error_message = "Contact already exists!."
                return jsonify({'error_message': error_message}), 400
            
        
            # Try a new way to get the 'user_id', like by joininng the two tables toghether then extracting the user_id where name is 'Mohamed' --for example
            new_relationship = Relationships(user_id=current_user_id, contact_id=contact_id)
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
                
        
        response_object = {'status':'success', 'contacts': contacts_list}

        return jsonify(response_object)
    
    elif request.method == "POST":
        
        post_data = request.get_json()
    
        try: 
            selected_year   = post_data.get('selectedYear')
            selected_month_num   = post_data.get('selectedMonth')
            selected_day  = post_data.get('selectedDay')
            submittedAmount  = post_data.get('submittedAmount')
            singedAmount  = post_data.get('singedAmount')
            contact_phone  = post_data.get('newContactPhone')
            transaction_note = post_data.get('transactionNote')
            
            print('submittedAmount', submittedAmount)
            print('singedAmount', singedAmount)
            # Please rebuild the db mopdels, in order to maek the app doesn't accept empty category
            
            if session.get('csrf_token') != request.cookies.get('csrfToken'):
                error_message = 'Unathorised access'
                return jsonify({'error_message': error_message}), 400
            
            
                
            if not all([selected_year, selected_month_num, selected_day, submittedAmount, contact_phone]):
                    error_message = 'All fields are required'
                    return jsonify({'error_message': error_message}), 400
                
            datetime(int(selected_year), int(selected_month_num), int(selected_day))
            
            if submittedAmount.find('+') == 0 or submittedAmount.find('-') == 0:
                error_message = 'Please type a transaction amount without a sign like "+" or "-" and then choose "Debt" or "Credit" !'
                return jsonify({'error_message': error_message}), 400
            
            submittedAmount = float(submittedAmount)
            
            if submittedAmount <= 0:
                error_message = 'Transaction Amount must be a positive number !'
                return jsonify({'error_message': error_message}), 400
            
            if singedAmount.find('+') == -1 and singedAmount.find('-') == -1:
                error_message = 'Please choose "Debt" or "Credit" !'
                return jsonify({'error_message': error_message}), 400
            
            singedAmount = float(singedAmount)
            
            if not bool(transaction_note): 
                transaction_note = None
            elif bool(transaction_note): 
                transaction_note = transaction_note.strip()
                                
        except Exception as e:
            print(e)
            error_message = 'Please Enter a valid Data'
            return jsonify({'error_message': error_message}), 400
    
        try:
            
            submitted_integer_amount = app.helpers.convert_float_to_int(singedAmount)

            new_contact_id = db.session.query(Contacts.id).filter(Contacts.phone==contact_phone).scalar()
            
            new_transactions = Transactions(amount=submitted_integer_amount, date=datetime(selected_year, selected_month_num, selected_day), user_id=current_user_id, contact_id=new_contact_id, note=transaction_note)
            
            db.session.add(new_transactions)
            
            db.session.commit()
            
            submitted_amount_as_egp_currency = app.helpers.egp(singedAmount)
            
            contact_name = db.session.query(Contacts.name).filter(Contacts.phone==contact_phone).scalar()
            
            response_object = {'submittedAmount': submitted_amount_as_egp_currency, 'submittedContactName':contact_name}
            
            return jsonify(response_object)
        
        except Exception as e:
            
            db.session.rollback()
            
            error_message = 'An error occurred while adding the expense! Error message: ' + str(e)
            return jsonify({'error_message': error_message}), 400
        
        finally:
            
            db.session.close()
