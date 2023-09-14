from datetime import datetime, timedelta
from app.models import db, Users, UsersSpendings, UsersWallets
from sqlalchemy import extract, func, and_

def egp(value):
    """Format value as USD."""
    return f"{value:,.2f} EGP"


def create_db():
    
    db.create_all()
    
    user_Emad = Users(name="Emad Eiad", username="emad12", phone="01100")
    
    user_salah = Users(name="Ahmed Salah", username="salah12", phone="0100")
    
    user_mark = Users(name="Mark Mork", username="mork12", phone="0121012")
    
    db.session.add(user_Emad)
    db.session.add(user_salah)
    db.session.add(user_mark)

    db.session.commit()
    
def add_wallet():
    
    emad_first = Users.query.filter_by(name="Emad Eiad").first()
    print('emad_first', emad_first)
    emad_id = Users.query.filter_by(name="Emad Eiad").first().user_id
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    mark_id = Users.query.filter_by(name="Mark Mork").first().user_id
    
    print(salah_id)
    print(mark_id)
    
    
    emad_wallet = UsersWallets(user_id=emad_id, balance=int(3000*100), debt=int(200*100), credit=int(300*100))
    salah_wallet = UsersWallets(user_id=salah_id, balance=int(8000*100), debt=int(1000*100), credit=int(2000*100))
    mark_wallet = UsersWallets(user_id=mark_id, balance=int(5000*100), debt=int(200*100), credit=int(300*100))
    
    
    db.session.add(emad_wallet)
    db.session.add(salah_wallet)
    db.session.add(mark_wallet)
    
    db.session.commit()
    
    print(emad_wallet, salah_wallet, mark_wallet)

def show_wallet():
    wallet  = db.session.query(UsersWallets).filter(UsersWallets.user_id == 2).first()
        
    wallet.balance = egp(wallet.balance/100)
    wallet.debt = egp(wallet.debt/100)
    wallet.credit = egp(wallet.credit/100)
    
    print('wallet.balance:', wallet.balance, 'wallet.debt:', wallet.debt, 'wallet.credit:', wallet.credit)
    
def pop_spend():
    
    db.session.query(UsersSpendings).delete()
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    monthStart = 9
    monthEnd = 10
    monthStep = 1
    dayStart = 4
    dayEnd = 5
    dayStep = 1
    
    spendings_dates = []
    
    # for month in range(monthStart, monthEnd, monthStep):
    #     for day in range(dayStart, dayEnd, dayStep):
    #         spending_date = datetime(2020, month, day).date()
    #         spendings_dates.append(spending_date)
            
    # for month in range(monthStart, monthEnd, monthStep):
    #     for day in range(dayStart, dayEnd, dayStep):
    #         spending_date = datetime(2023, month, day).date()
    #         spendings_dates.append(spending_date)
            

    
    # for date in spendings_dates:
        # salah_spendings = UsersSpendings(user_id=salah_id, amount_spent=40, category="Bills", date=date.date())
        
    spend_date = datetime()
    
    amounts = [100, 140, 200, 143, 334, 234, 452, 233]
    
    for amount in amounts:
        salah_spendings = UsersSpendings(user_id=salah_id, amount_spent=amount, category="Bills", date=datetime.now())        
        db.session.add(salah_spendings)
        
    for amount in amounts:
        salah_spendings = UsersSpendings(user_id=salah_id, amount_spent=amount, category="Car", date=datetime.now())
        db.session.add(salah_spendings)
        
    for amount in amounts:
        salah_spendings = UsersSpendings(user_id=salah_id, amount_spent=amount, category="Food", date=datetime.now())            
        db.session.add(salah_spendings)
    
    
    specific_date = datetime(2023, 9, 6)
    start_of_day = specific_date
    end_of_day = specific_date + timedelta(days=1)
    
     # Modify the query to include the sum calculation and group by day
    user_spendings_today = UsersSpendings.query.filter(and_(UsersSpendings.user_id == salah_id, UsersSpendings.date >= start_of_day, UsersSpendings.date < end_of_day)).order_by(UsersSpendings.date.desc()).all()
    
    [print(spending) for spending in user_spendings_today]
    
def pop_spend2():
    
    # Assuming 'db' is your SQLAlchemy instance
    date_to_insert = datetime(2022, 1, 5)

    # Generate 10 different times on the same date
    time_intervals = [timedelta(hours=i) for i in range(8)]

    spending_time_list = []
    
    for time_interval in time_intervals:
        spending_time = date_to_insert + time_interval
        spending_time_list.append(spending_time)
        
    amounts = [100, 140, 200, 143, 334, 234, 452, 233]
    
    categories = ['Bills', 'Car', 'Clothes', 'Communication', 'Eating out', 'Entertainment', 'Food', 'Gifts']
    
    for amount, spending_time, category in zip(amounts, spending_time_list, categories):
        salah_spendings = UsersSpendings(
            user_id=2,
            amount_spent=amount,
            category=category,
            date=spending_time
        )
        
        db.session.add(salah_spendings)
    
    
    db.session.commit()
    
    user_spendings = db.session.query(UsersSpendings).filter(UsersSpendings.user_id == 2)
    
    [print(spending) for spending in user_spendings]
    
    
    
    
    
def show_spend():
    
    salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id
    
    # # Get all spendings for Ahmed in the year 2020
    # start_date = datetime(2020, 1, 1)
    # end_date = datetime(2020, 12, 31)
    # salah_spendings_2020 = UsersSpendings.query.filter_by(user_id=salah_id).filter(UsersSpendings.date >= start_date, UsersSpendings.date <= end_date).all()
    
    # for spend_day in salah_spendings_2020:
    #     print(f'Spending ID: {spend_day.spending_id}')
    #     print(f'User ID: {spend_day.user_id}')
    #     print(f'Date: {spend_day.date}')
    #     print(f'amount: {spend_day.amount_spent}')
    #     print(f'Item Type: {spend_day.category}')
    #     print()

    specific_date = datetime(2023, 9, 6)
    start_of_day = specific_date
    end_of_day = specific_date + timedelta(days=1)
     
    user_spendings_today = UsersSpendings.query.filter(and_(UsersSpendings.user_id == salah_id, UsersSpendings.date >= start_of_day, UsersSpendings.date < end_of_day)).order_by(UsersSpendings.date.desc()).all()
    
    [print(spending) for spending in user_spendings_today]
    
    # user_spendings = UsersSpendings.query.filter_by(user_id= 2).all()
    # [print(spending) for spending in user_spendings]


        
    
    
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
    
    month_spendings_list = [{'spending_id': spending.spending_id, 'user_id': spending.user_id, 'date': spending.date, 'amount_spent': spending.amount_spent, 'category': spending.category} for spending in MonthSpendings]
    
    # [print(spending) for spending in month_spendings_list]
    
    for spending in month_spendings_list:
        print("spending['date']", spending['date'])
        
    print('month_spendings_list', month_spendings_list)
    
    for spend in MonthSpendings:
        print("spend.date", spend.date)
        
def total_d_spend():
    
    daily_spendings = db.session.query(
        func.date(UsersSpendings.date).label("spending_date"),
        func.sum(UsersSpendings.amount_spent).label("total_spent")
    ).filter(UsersSpendings.user_id == 2).\
        group_by("spending_date").\
        order_by("spending_date").all()
    
    for date, total_spent in daily_spendings:
        print(f"Date: {date}, Total Spent: {total_spent}")
    
    [print(spending) for spending in month_spendings]
    
def show_days():
    days = UsersSpendings.query.filter(UsersSpendings.user_id == 2).group_by(extract('month', UsersSpendings.date)).order_by(extract('day', UsersSpendings.date).desc()).all()
    
    # print(days)
    
    # [print(f"day.date: {day.date}") for day in days]
    
    # print(extract('day', UsersSpendings.date))
    
    tests = UsersSpendings.query.filter(extract('day', UsersSpendings.date)).order_by(extract('day', UsersSpendings.date).desc()).all()
    # [print(f"day.date: {test.date}") for test in tests]
    
    

def test ():
    years = UsersSpendings.query.with_entities(
                extract('year', UsersSpendings.date)
            ).filter(
                UsersSpendings.user_id == 2
            ).group_by(
                extract('year', UsersSpendings.date)
            ).order_by(
                extract('year', UsersSpendings.date).desc()
            ).all()
            
    # years[0] this will access the first value/element in the tuple of 'year' in 'years' list
    years = [year[0] for year in years]
    
    print(years)
    
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
                
        years_and_months.append({'year': year, 'months': months_list})
        
    print(years_and_months)
    
    # [print("year:", year) for (year) in years_and_months]
    
    
    # for year in years_and_months:
    #     for month in years_and_months[year]:
    #         str_month = datetime(1, month, 1).strftime('%b')
    #         months_as_abbr.append(str_month)
    # return months_as_abbr
    
def test2 ():
    months = UsersSpendings.query.with_entities(
            extract('month', UsersSpendings.date)
        ).filter(
            UsersSpendings.user_id == 2
        ).filter(
            extract('year', UsersSpendings.date) == 2022
        ) .group_by(
            extract('month', UsersSpendings.date)
        ).order_by(
            extract('month', UsersSpendings.date).desc()
        ).all()
    
    print('months:', months)