from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<User Name %r>' % self.name
    
class UserSpending(db.Model):
    __tablename__ = 'users_spendings'
    spending_id = db.Column(db.Integer, primary_key=True)
    # Define the foreign key column
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, default=datetime.now(), nullable=False)
    item_type = db.Column(db.String(64), unique=False)

    # Define the relationship between UserSpending and User
    user = db.relationship('User', backref=db.backref('spendings', lazy=True))
    
    def __repr__(self):
        return '<Spending ID %r>' % self.spending_id
    
    
    """
    # Some commands that I will execute in flask shell:
    - 
    """