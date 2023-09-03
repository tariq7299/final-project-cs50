from flask import request, jsonify, Blueprint
from app.models import db, Users, UsersSpendings
from datetime import datetime
from sqlalchemy import extract, func


appRoutes = Blueprint("routes", __name__)

# @<bluebrint name>.route()
@appRoutes.route("/spendings", methods=["POST","GET"])
def spendings():
    
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

        total_monthly_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == most_recent_year).filter(extract('month', UsersSpendings.date) == most_recent_month).scalar()
        
        # print(total_monthly_spendings)
        
        # total_daily_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == most_recent_year).filter(extract('month', UsersSpendings.date) == most_recent_month).filter().group_by(extract('day', UsersSpendings.date)).order_by(UsersSpendings.date.desc()).all()
        
        # total_daily_spendings_list = [{'total_daily_spending': row[0]} for row in total_daily_spendings]
        
        # print("total_daily_spendings", total_daily_spendings_list)
        # print("month_spendings", month_spendings)
        
        month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'item_type': spending.item_type} for spending in month_spendings]
        
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
        
        response_object['monthSpendings'] = month_spendings_list
        
        response_object['total_monthly_spendings'] = total_monthly_spendings
        
        # response_object['total_daily_spendings'] = total_daily_spendings_list
        
        # Return response object as JSON∆
        return jsonify(response_object)
    
# @<bluebrint name>.route()
@appRoutes.route("/RecentMonthSpendings", methods=["POST","GET"])
def RecentMonthSpendings():
    
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
            
        month_spendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).order_by(UsersSpendings.date.desc()).all()
    
        month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'item_type': spending.item_type} for spending in month_spendings]
        
        total_monthly_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).scalar()

        # total_daily_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == most_recent_month).filter().group_by(extract('day', UsersSpendings.date)).order_by(extract('month', UsersSpendings.date).desc()).all()

        # total_daily_spendings_list = [{'total_daily_spending': row[0]} for row in total_daily_spendings]

        response_object['total_monthly_spendings'] = total_monthly_spendings

        
        # response_object['total_daily_spendings'] = total_daily_spendings_list

        response_object['months'] = str_month_list
        response_object['monthSpendings'] = month_spendings_list

        # Return response object as JSON
        return jsonify(response_object)
    
# @<bluebrint name>.route()
@appRoutes.route("/selectedMonthSpendings", methods=["POST","GET"])
def selectedMonthSpendings():
    
    # Replace this user id from by the one foumd in session['user_id']
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    response_object = {'status':'success'}
    
    if request.method == "POST":
            
        post_data = request.get_json()
        
        selected_year   = post_data.get('selectedYear')
        selected_month_str   = post_data.get('selectedMonth')
        selected_month_int = datetime.strptime(selected_month_str, '%b').month

        month_spendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == selected_month_int).order_by(UsersSpendings.date.desc()).all()
        
    
        month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date.strftime('%b %d, %Y'), 'amount_spent': spending.amount_spent, 'item_type': spending.item_type} for spending in month_spendings]
        
        total_monthly_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == selected_month_int).scalar()

        # total_daily_spendings = db.session.query(func.sum(UsersSpendings.amount_spent)).filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == selected_year).filter(extract('month', UsersSpendings.date) == selected_month_int).filter().group_by(extract('day', UsersSpendings.date)).order_by(extract('month', UsersSpendings.date).desc()).all()

        # total_daily_spendings_list = [{'total_daily_spending': row[0]} for row in total_daily_spendings]
# 
        # response_object['total_daily_spendings'] = total_daily_spendings_list

        
        response_object['total_monthly_spendings'] = total_monthly_spendings

        response_object['monthSpendings'] = month_spendings_list

        
        
        # Return response object as JSON
        return jsonify(response_object)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
        
