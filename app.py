from cs50 import SQL

from flask import redirect, render_template, session
# This is used inside of @ deceorator functions, to not not make the deceorated functins lose its __name__
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
print("hello world")
print("hello world")
print("hello world")
print("hello world")


def validate_password(password):
    import re # regular expression
    if len(password) < 8:
        return ("Password should be at least 8 characters or longer")
    elif not re.search("[0-9]", password):
        return ("Password must contain at least one digit")
    elif not re.search("[A-Z]", password):
        return ("Password must contain at least one uppercase letter")
    elif not re.search("[@_!#$%&^*()<>?~+-/\{}:]",password):
        return ("password must contain at least one special charaster")
    
def extract_user_stocks_from_db(current_user_id):
    return db.execute("SELECT ROW_NUMBER() OVER (ORDER BY shares DESC) AS RowNumber, stock_symbol, shares FROM users_stocks WHERE user_id = ?", current_user_id)

def extract_shares_owned_by_user(current_user_id, quote_symbol):
    return db.execute("SELECT shares FROM users_stocks WHERE user_id = ? AND stock_symbol = ?", current_user_id, quote_symbol)[0]['shares']

def extract_latest_five_user_transactions(current_user_id):
    return db.execute("SELECT ROW_NUMBER() OVER (ORDER BY transaction_date DESC) AS RowNumber, transaction_id, transaction_date, quote_symbol, price_per_share, shares, holding_value, trading_fees, total_amount, transaction_type FROM transactions WHERE user_id = ? LIMIT 5", current_user_id)

def extract_all_user_transactions(current_user_id):
    return db.execute("SELECT ROW_NUMBER() OVER (ORDER BY transaction_date DESC) AS RowNumber, transaction_id, transaction_date, quote_symbol, price_per_share, shares, holding_value, trading_fees, total_amount, transaction_type FROM transactions WHERE user_id = ?", current_user_id)


print("text")
print("text")

print("text")






print("text")
print("text")
print("text")
print("text")

# "second commit"
print("text")
print("text")

# testing 5
print("letsgooooo")

# testing 6
print("loooooo")


# things changed in the letsgoo branch
print("Claskyyy")


# plsdiosidj
print("shlusky")

