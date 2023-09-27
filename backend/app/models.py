from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)


class Users(db.Model):
    
    __table_args__ = (
        
        db.UniqueConstraint('user_id', name='unique_user_id'),
        db.UniqueConstraint('username', name='unique_username'),
        db.UniqueConstraint('email', name='unique_email')
    )
    
    # # Acutally  no mre need to specifiy "__tablename__" as it actully converts thw CamelCase "Users" to a snake_case "users" and make it as the table name
    # __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    hash = db.Column(db.String(81), nullable=False)
    
    
    def __repr__(self):
        return '<User ID: {}, First Name: {}, Last Name: {}, username: {}, email: {}, hash: {}>'.format(self.user_id, self.first_name, self.last_name, self.username, self.email, self.hash)
    
# I found out that the best way to store money values in sqlite db, si by specifiyng the column type as 'Integer', and when I want to lets say store "3.59" i store like that int(3.59 * 100) so it will be stored like that "359", and when I want to retrive the value I do that '359/100' so the value will be converted to floasting number once more '3.59' ! 
class UsersWallets(db.Model):
    
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
        CheckConstraint('debt >= 0', name='check_money_user_owe_non_negative'),
        CheckConstraint('credit >= 0', name='check_money_owed_to_user_non_negative'),
        db.UniqueConstraint('user_id', name='unique_user_id')
    )
    
    wallet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)
    debt = db.Column(db.Integer, default=0, nullable=False)
    credit = db.Column(db.Integer, default=0, nullable=False)
    user = db.relationship('Users', backref=db.backref('wallet', lazy=True))
    
    def __repr__(self):
        return f'UsersWallets(wallet_id={self.wallet_id}, user_id={self.user_id}, balance={self.balance/100}, debt={self.debt/100}, credit={self.credit/100})'
class UsersSpendings(db.Model):
    spending_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount_spent = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False) 
    note = db.Column(db.String(200), default="No notes")
    user = db.relationship('Users', backref=db.backref('spendings', lazy=True))

    def __repr__(self):
        return '<Spending ID: {}, User ID: {}, Date: {}, Amount Spent: {}, Category: {}>'.format(self.spending_id, self.user_id, self.date, self.amount_spent, self.category_id) 

class Categories(db.Model): 
    
    # This should be a tuple
    __table_args__ = (db.UniqueConstraint('name', name='unique_category_name'),)
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(64), nullable=False, unique=True)
   
class Contacts(db.Model):
    
    # This should be a tuple
    __table_args__ = (db.UniqueConstraint('phone', name='unique_contact_phone'),)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Contact ID: {}, Contact_Name: {}, Contact_phone: {}>'.format(self.id, self.name, self.phone)
        
class UserCategory(db.Model):
    
    __table_args__ = (db.UniqueConstraint('user_id', 'category_id', name='unique_user_category'),)
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('user_categories', lazy=True))
    category = db.relationship('Categories', backref=db.backref('user_categories', lazy=True))
class Relationships(db.Model):
    
    __table_args__ = (db.UniqueConstraint('user_id', 'contact_id', name='unique_user_contact'),)
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    
    def __repr__(self):
        return '<Relationship ID: {}, User_id: {}, Contact_id: {}>'.format(self.id, self.user_id, self.contact_id)
    
    user = db.relationship('Users', backref=db.backref('user_relationships'), lazy=True)
    
    contact = db.relationship('Contacts', backref=db.backref('contact_relationships'), lazy='joined')
    
class Transactions(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    note = db.Column(db.String(200), default="No notes", nullable=False)
    # By definning a relationship you can now access the user info from 'Users' model, by typing 'Transactions.user'
    # And Vice versa, so  "backref=db.backref('user_transactions')" enables you to access user transactions from 'Users'db model, by typing "Users.user_transactions"
    # lazy=joined and lazy=True are the same (They supposed to not be the same, but I still can't understand the difference )
    # lazy enables you to access all columns of 'Users' and 'Transactions', without using join() in the query
    
    user = db.relationship('Users', backref=db.backref('user_transactions'), lazy=True)
    
    contact = db.relationship('Contacts', backref=db.backref('contact_transactions'), lazy='joined')
    
    def __repr__(self):
        return '<Transaction ID: {}, Amount: {}, Date: {}, User ID: {}, User Name: {}, Contact ID: {}, Contact Name: {}>'.format(self.id, self.amount, self.date, self.user_id, self.user.name, self.contact_id, self.contact.name)
    
    