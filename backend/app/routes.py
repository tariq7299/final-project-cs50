from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings
from datetime import datetime


appRoutes = Blueprint("routes", __name__)

# @<bluebrint name>.route()
@appRoutes.route("/fetchYears", methods=["POST","GET"])
def submitData():
    response_object = {'status':'success'}
    if request.method == "GET":
        
        # Take user id from session['user_id']
        salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id

        
        # Get all spendings for Ahmed in the year 2020
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 12, 31)
        salah_spendings_2020 = UsersSpendings.query.filter_by(user_id=salah_id).filter(UsersSpendings.date >= start_date, UsersSpendings.date <= end_date).all()
        
        # Convert the spendings data to a list of dictionaries
        spendings_data = []
        for spending in salah_spendings_2020:
            spending_dict = {
                'spending_id': spending.spending_id,
                'user_id': spending.user_id,
                'date': spending.date,
                'item_type': spending.item_type
            }
            spendings_data.append(spending_dict)

        # Return the spendings data as a JSON response
        return jsonify(spendings_data)
        
        
    

# @<bluebrint name>.route()
@appRoutes.route("/dataentry2", methods=["POST","GET"])
def submitData2():
    response_object = {'status':'success'}
    if request.method == "POST":
        post_data = request.get_json()
        company   = post_data.get('company'),
        print(company)
        response_object['message'] ='Data added!'
        
        # You can do this 
        response_object['message'] ='Data added!'
        response_object['company'] = company
    
        print(response_object)
    return jsonify(response_object)

# @<bluebrint name>.route()
@appRoutes.route("/showUsers", methods=["POST","GET"])
def showUsers():
    response_object = {'status':'success'}
    if request.method == "POST":
        post_data = request.get_json()
        company   = post_data.get('company'),
        print(company)
        response_object['message'] ='Data added!'
        
        # You can do this 
        response_object['message'] ='Data added!'
        response_object['company'] = company
    
        print(response_object)
    return jsonify(response_object)
    

        ## some very important notes:
"""
However, if you need to access the SECRET_KEY or any other configuration value within your routes, you can import them from app.config in your routes.py file:

from app import app  # Import the 'app' instance from __init__.py
from flask import request, jsonify

@app.route("/dataentry", methods=["POST", "GET"])
def submitData():
    secret_key = app.config.get("SECRET_KEY")
    # ... your route logic ...
    
            &#&&#&&#&#&#&#&#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$$#$#$#
            
You should not import anything from the run.py or config.py files in your routes.py file. These files are used to run and configure your Flask application, respectively. They should not be imported by your routes or view functions.

If you have defined any custom modules or objects that are required by your route and view function, you can import them in your routes.py file as well. For example, if you have defined a custom database model in a separate module, you can import it like this:

from mymodule import MyModel
    
"""