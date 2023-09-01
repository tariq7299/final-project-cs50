from datetime import datetime
from app.models import db, Users, UsersSpendings

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
    
    monthStart = 1
    monthEnd = 5
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
    
