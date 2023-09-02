from datetime import datetime
from app.models import db, Users, UsersSpendings
from sqlalchemy import extract, func

def create_db():
    
    db.create_all()
    
    user_Emad = Users(name="Emad Eiad", username="emad12", phone="01100")
    
    user_salah = Users(name="Ahmed Salah", username="salah12", phone="0100")
    
    user_mark = Users(name="Mark Mork", username="mork12", phone="0121012")
    
    db.session.add(user_Emad)
    db.session.add(user_salah)
    db.session.add(user_mark)

    db.session.commit()
    
    emad_id = Users.query.filter_by(name="Emad Eiad").first().user_id
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    mark_id = Users.query.filter_by(name="Mark Mork").first().user_id
    
    emad_spendings = UsersSpendings(user_id=emad_id, amount_spent="200", item_type="food")
    
    salah_spendings = UsersSpendings(user_id=salah_id, amount_spent="40", item_type="seed")
    
    mark_spendings = UsersSpendings(user_id=mark_id, amount_spent="90", item_type="need")
    
    db.session.add(emad_spendings)
    db.session.add(salah_spendings)
    db.session.add(mark_spendings)
    
    db.session.commit()
    
    print(user_Emad, user_salah, user_mark)
        
    

def show_spend():
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    # Get all spendings for Ahmed in the year 2020
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)
    salah_spendings_2020 = UsersSpendings.query.filter_by(user_id=salah_id).filter(UsersSpendings.date >= start_date, UsersSpendings.date <= end_date).all()
    
    for spend_day in salah_spendings_2020:
        print(f'Spending ID: {spend_day.spending_id}')
        print(f'User ID: {spend_day.user_id}')
        print(f'Date: {spend_day.date}')
        print(f'amount: {spend_day.amount_spent}')
        print(f'Item Type: {spend_day.item_type}')
        print()

        

def pop_spend():
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    monthStart = 9
    monthEnd = 10
    monthStep = 1
    dayStart = 1
    dayEnd = 20
    dayStep = 1
    
    spendings_dates = []
    
    for month in range(monthStart, monthEnd, monthStep):
        for day in range(dayStart, dayEnd, dayStep):
            spending_date = datetime(2020, month, day).date()
            spendings_dates.append(spending_date)
            
    for month in range(monthStart, monthEnd, monthStep):
        for day in range(dayStart, dayEnd, dayStep):
            spending_date = datetime(2023, month, day).date()
            spendings_dates.append(spending_date)
            
    for date in spendings_dates:
        
        salah_spendings = UsersSpendings(user_id=salah_id, amount_spent="40", item_type="Food", date=date)
                    
        db.session.add(salah_spendings)
    
    db.session.commit()
    
def show_years():
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    result = db.session.query(
        extract('year', UsersSpendings.date)
    ).filter(
        UsersSpendings.user_id == salah_id
    ).group_by(
        extract('year', UsersSpendings.date)
    ).all()
    
    # Same but with the usage of ClassName.query()
    """
        result = UsersSpendings.query.with_entities(
                extract('year', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == mark_id
            ).group_by(
                extract('year', UsersSpendings.date)
            ).all()
            
        ------> # A note about with_entities()
        In this example, we use the with_entities() method to specify that we want to select only the date and amount_spent columns from the UsersSpendings table. The result is a list of tuples where each tuple contains the values of these two columns for one row.
        result = UsersSpendings.query.with_entities(
            UsersSpendings.date,
            UsersSpendings.amount_spent
        ).all()

        # Print the result
        for date, amount_spent in result:
            print(f'Date: {date}, Amount Spent: {amount_spent}')
    """
    # Print the result
    print('result is ', result)
    for year, in result:
        print(f'Year: {year}')
        
def show_months():
    
    selected_year   = 2023
    
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
        ).all()

    str_month_list = []
    for int_month, in months:
        str_month = datetime(1, int_month, 1).strftime('%b')
        str_month_list.append(str_month)

    [print(month) for month in str_month_list]
    
def month_spendings():
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
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
    print("most_recent_year", most_recent_year)
            
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
    print("most_recent_month", most_recent_month)
            
    MonthSpendings = UsersSpendings.query.filter(UsersSpendings.user_id == salah_id).filter(extract('year', UsersSpendings.date) == most_recent_year).filter(extract('month', UsersSpendings.date) == most_recent_month).order_by(UsersSpendings.date.desc()).all()
    
    print("MonthSpendings", MonthSpendings)
    for spend in MonthSpendings:
        print("spend", spend)
        print(spend.date, spend.amount_spent)
        