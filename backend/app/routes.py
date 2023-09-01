from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings
from datetime import datetime
from sqlalchemy import extract, func


appRoutes = Blueprint("routes", __name__)

# @<bluebrint name>.route()
@appRoutes.route("/fetchYears", methods=["POST","GET"])
def fetchYears():
    response_object = {'status':'success'}
    if request.method == "GET":
        
        # Replace this user id from by the one foumd in session['user_id']
        salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id

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
        
        # Add years data to response object
        # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
        response_object['years'] = [year[0] for year in years]
        print(response_object['years'])
    # Return response object as JSON
    return jsonify(response_object)
        
@appRoutes.route("/fetchMonths", methods=["POST","GET"])
def fetchMonths():
    response_object = {'status':'success'}
    if request.method == "POST":
        
        post_data = request.get_json()
        selected_year   = post_data.get('selectedYear')
        
        # Replace this user id from by the one foumd in session['user_id']
        salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id

        # extract() is used to get the years from date object !, of the column 'date' of type 'db.date'
        # with_entities() It gets specific columns only
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
            
        # Add years data to response object
        # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
        print(selected_year)
        response_object['months'] = str_month_list
        
    # Return response object as JSON
    return jsonify(response_object)
        
