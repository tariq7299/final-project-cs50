from flask_sqlalchemy import SQLAlchemy, CheckConstraint
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)


class Users(db.Model):
    
    # # Acutally  no mre need to specifiy "__tablename__" as it actully converts thw CamelCase "Users" to a snake_case "users" and make it as the table name
    # __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<User ID: {}, Name: {}, username: {}, phone: {}>'.format(self.user_id, self.name, self.username, self.phone)
    
    
class UsersWallets(db.Model):
    
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
        CheckConstraint('debt >= 0', name='check_money_user_owe_non_negative'),
        CheckConstraint('credit >= 0', name='check_money_owed_to_user_non_negative')
    )
    
    wallet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Numeric, default=0, nullable=False)
    debt = db.Column(db.Numeric, default=0, nullable=False)
    credit = db.Column(db.Numeric, default=0, nullable=False)
    user = db.relationship('Users', backref=db.backref('wallet', lazy=True))
    
    def __repr__(self):
        return f'UsersWallets(wallet_id={self.wallet_id}, user_id={self.user_id}, balance={self.balance})'
class UsersSpendings(db.Model):
    
    # Acutally  no mre need to specifiy "__tablename__" as it actully converts thw CamelCase "UsersSpendings" to a snake_case "users_spendings" and make it as the table name
    # __tablename__ = 'users_spendings'
    spending_id = db.Column(db.Integer, primary_key=True)
    # Define the foreign key column
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, default=datetime.now().date(), nullable=False)
    amount_spent = db.Column(db.Numeric, nullable=False)
    category = db.Column(db.String(64), unique=False)
    # Define the relationship between UserSpending and User
    user = db.relationship('Users', backref=db.backref('spendings', lazy=True))
    
    def __repr__(self):
        return '<Spending ID: {}, User ID: {}, Date: {}, Amount Spent: {}, Category: {}>'.format(self.spending_id, self.user_id, self.date, self.amount_spent, self.category)
    
    
    """
    # Some commands that I will execute in flask shell:
    - 
    """