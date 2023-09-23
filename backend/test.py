from datetime import datetime, timedelta
from app.models import db, Users, UsersSpendings, UsersWallets, Contacts, Relationships, Transactions, Categories
from sqlalchemy import extract, func, and_
import app.helpers

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
    

def wallet2():
    
    total_net_balance = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==2).scalar()

    print('total_net_balance', app.helpers.convert_int_to_float(total_net_balance))

    debt = 0
    credit = 0
    
    net_balance_per_contact = db.session.query(func.sum(Transactions.amount).label('contact_net_balance')).filter(Transactions.user_id==2).group_by(Transactions.contact_id).all()
    
    print('net_balance_per_contact-->', net_balance_per_contact)

    [print('net-->', net) for net in net_balance_per_contact]
    
    for net_balance, in net_balance_per_contact:
        if net_balance > 0:
            credit += net_balance
        else:
            debt += net_balance
    
    print('credit', app.helpers.convert_int_to_float(credit))
    print('debt', app.helpers.convert_int_to_float(debt))
     

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

    categories_id = ['1', '2', '3', '4', '5', '6', '7', '8']

    for amount, spending_time, category_id in zip(amounts, spending_time_list, categories_id):
        salah_spendings = UsersSpendings(
            user_id=2,
            amount_spent=amount,
            category_id=category_id,
            date=spending_time
        )
        
        db.session.add(salah_spendings)


    db.session.commit()

    user_spendings = db.session.query(UsersSpendings).filter(UsersSpendings.user_id == 1)

    [print(spending) for spending in user_spendings]

# def rel_Db():

    # salah_rel = Relationships(user_id=2, contact_id=3)
    # salah_rel2 = Relationships(user_id=2, contact_id=2)
    # emad_rel = Relationships(user_id=1, contact_id=1)

    # db.session.add(salah_rel)
    # db.session.add(salah_rel2)
    # db.session.add(emad_rel)

    # db.session.commit()

    # print(salah_rel)
    # print(salah_rel2)
    # print(emad_rel)
    
    
    
    
    
def show_spend():

    # salah_id = Users.query.filter_by(name="Ahmed Salah").first().user_id

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

    # specific_date = datetime(2023, 9, 6)
    # start_of_day = specific_date
    # end_of_day = specific_date + timedelta(days=1)
        
    # user_spendings_today = UsersSpendings.query.filter(and_(UsersSpendings.user_id == salah_id, UsersSpendings.date >= start_of_day, UsersSpendings.date < end_of_day)).order_by(UsersSpendings.date.desc()).all()
    
    user_spendings_today = db.session.query(UsersSpendings, Categories.name).join(Categories, UsersSpendings.category_id == Categories.id).filter(UsersSpendings.user_id == 25, extract('year', UsersSpendings.date) == 2023, extract('month', UsersSpendings.date) == 9).order_by(UsersSpendings.spending_id.desc()).all()

    # [print(spending) for spending in user_spendings_today]
    
    month_expenses_list = [{'spending_id': tuple[0].spending_id, 'user_id': tuple[0].user_id, 'date': tuple[0].date.strftime("%a %d/%m/%Y"), 'amount_spent': app.helpers.convert_int_to_float(tuple[0].amount_spent), 'category': tuple[1], 'note': tuple[0].note} for tuple in user_spendings_today]

    # [print(spending, category_name) for spending, category_name in user_spendings_today]
    
    [print(spending) for spending in month_expenses_list]
    
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
        
def pop_contacts():
    
    db.create_all()
    
    # contact_shawn = Contacts(name="Koftes Shawn", phone="01086767536")
    # contact_sobhy = Contacts(name="Khaled Sobhy", phone="01084682636")
    contact_shaba7 = Contacts(name="Abdelrahman SHABA7", phone="01083er2336")
    contact_keke = Contacts(name="Abdelrahman keke", phone="01083er2656")
    contact_foo= Contacts(name="foo ElShabah", phone="0108322asd36")
    contact_ahmed = Contacts(name="Ahemd kaherfs", phone="010832242336")
    contact_soso = Contacts(name="lop", phone="01874y623")
    contact_ElShfah = Contacts(name="Moataz dodo", phone="047y73")
    contact_moo = Contacts(name="moo ElShabah", phone="01083cd36")
    contact_spider = Contacts(name="Lizard Spider MOOn", phone="0102322336")
    
    contacts = []
    # contacts.append(contact_shawn)
    # contacts.append(contact_sobhy)
    contacts.append(contact_shaba7)
    contacts.append(contact_keke)
    contacts.append(contact_foo)
    contacts.append(contact_ahmed)
    contacts.append(contact_soso)
    contacts.append(contact_ElShfah)
    contacts.append(contact_moo)
    contacts.append(contact_spider)
    
    # db.session.add(contact_shawn)
    # db.session.add(contact_sobhy)
    db.session.add(contact_shaba7)
    db.session.add(contact_keke)
    db.session.add(contact_foo)
    db.session.add(contact_ahmed)
    db.session.add(contact_soso)
    db.session.add(contact_ElShfah)
    db.session.add(contact_moo)
    db.session.add(contact_spider)
    
    db.session.commit()
    
    [print(contact) for contact in contacts] 
    

def pop_transactions():
    
    # Assuming 'db' is your SQLAlchemy instance
    date_to_insert = datetime(2023, 9, 17)

    # Generate 10 different times on the same date
    time_intervals = [timedelta(hours=i) for i in range(8)]

    transactions_time_list = []

    for time_interval in time_intervals:
        transaction_time = date_to_insert + time_interval
        transactions_time_list.append(transaction_time)
        
    amounts = [-103, 140, -420, 543, -349, 234, -473, 233]
    
    

    for amount, transaction_time, contact_id in zip(amounts, transactions_time_list, range(1, 9, 1)):
        
        salah_transactions = Transactions(
            
            amount=amount,
            date=transaction_time,
            user_id=2,
            contact_id=contact_id,
        )
        
        db.session.add(salah_transactions)


    db.session.commit()

    user_transactions = db.session.query(Transactions).filter(Transactions.user_id == 2)

    [print(transaction) for transaction in user_transactions]
    
def test3():
    
    net_balances_all = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==2).all()
    net_balances_scalar = db.session.query(func.sum(Transactions.amount)).filter(Transactions.user_id==2).scalar()
    
    # [print(net_balance) for net_balance in net_balances]
    
    print(net_balances_all)
    print(net_balances_scalar)
    
def test4 ():
    
    
                        # The two are the same
                
                #   1- but the first tusing join() in the query iteself.
                #   2- An the second utilizing lazy=joined or lazy=True from defined in the 'Class Transactions' found in models.py
     
     
    #   1-  With using join(), without 'lazy' and 'relationship' defined in the Class
    
    transactions__join = db.session.query(Contacts.name, Contacts.phone, func.sum(Transactions.amount)).join(Contacts).filter(Transactions.user_id==2).group_by(Transactions.contact_id).all()
    
    # transactions = db.session.query(Transactions, func.sum(Transactions.amount).label('contact_net_balance')).join('Contacts').filter(Transactions.user_id==2).group_by(Transactions.contact_id).all()
    
    #   2- With utlizing the lazy=joined technique/feature (this defined in the model itself), then you access the 'contact name' and 'contact phone'
    
    transactions__lazy = db.session.query(Transactions, func.sum(Transactions.amount).label('contact_net_balance')).filter(Transactions.user_id==2).group_by(Transactions.contact_id).all()
    
    for transaction in transactions__lazy:
        print('transaction.contact_name__2', transaction[0].contact.name)
    #     print('transaction.contact_phone', transaction[0].contact.phone)
    #     print('transaction_amount', transaction.contact_net_balance)
    
                #%#$%#$%#$#%$#%$#%#$#%$#%#$%#$%#$#%$#%$#%#$%#$#%$#%
    
    
    
    
    
    
    # transactions_list = [{'contact_name': transaction[0].contact.name, 'contact_phone': transaction[0].contact.phone, 'transations_net_balance': transaction.contact_net_balance} for transaction in transactions__lazy] 
    
    # print('transactions_list', transactions_list)
    
    # THis way you can access 'Users'db table, from 'transaction', as it is 'Transactions' instence, this beacuse that line --> user = db.relationship('Users', backref=db.backref('user_transactions'), lazy=True)
    
    # transactions0 = db.session.query(Transactions).filter(Transactions.user_id==2).all()
    
    # for transaction in transactions0:
    #     print('transaction.user', transaction.user)
    #     print('transaction.contact', transaction.contact)
    #     print("###$$###")
    #     print('transaction.contact.name', transaction.contact.name)
    #     print('transaction.contact.phone', transaction.contact.phone)
    #     print()
    #     print("-----")
    #     print()
    
def CH():
    
    contact_phone = '01084682636'

    transactions__lazy = db.session.query(Transactions).filter(and_(Transactions.user_id==2), (Contacts.phone==contact_phone)).order_by(Transactions.date.desc()).join(Contacts)

    print('transactions', transactions__lazy)

    transactions_list = [{'date': transaction.date.strftime("%a %d/%m/%Y"), 'amount': transaction.amount} for transaction in transactions__lazy]

    [print('transaction $-->', transaction) for transaction in transactions_list]
    
    

def rel_Db():
    
    # salah_rel = Relationships(user_id=2, contact_id=3)
    # salah_rel2 = Relationships(user_id=2, contact_id=2)
    # emad_rel = Relationships(user_id=1, contact_id=1)
    
    # db.session.add(salah_rel)
    # db.session.add(salah_rel2)
    # db.session.add(emad_rel)
    
    # db.session.commit()
    
    # print(salah_rel)
    # print(salah_rel2)
    # print(emad_rel)
    
    contacts = db.session.query(Contacts).filter(Relationships.user_id==2).join(Relationships, Relationships.contact_id == Contacts.id).all()
    
    print('contacts', contacts)
     
    contacts_list = [{'contact_id': contact.id, 'contact_name': contact.name, 'contact_name': contact.name, 'contact_name': contact.name, 'contact_phone': contact.phone} for contact in contacts]
    
    print('contacts_list', contacts_list)

def pop_cat():
    categories = ['Bills', 'Car', 'Clothes', 'Communication', 'Eating out', 'Entertainment', 'Food', 'Gifts', 'Health', 'House', 'Kids', 'Sports', 'Transport']
    
    for C_name in categories:
        new_category = Categories(name=C_name)
        db.session.add(new_category)
    db.session.commit()
    
    
