from dotenv import load_dotenv
from os import environ

load_dotenv()


# So the below variables are imported from .env file !


SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')

# You can use this to define the path of sqlite database here instead of importing it from
# basedir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(basedir, 'instance', 'mydatabase.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path

SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
SESSION_TYPE = environ.get('SESSION_TYPE')
SESSION_COOKIE_SECURE = environ.get('SESSION_COOKIE_SECURE')
SESSION_COOKIE_SAMESITE = environ.get('SESSION_COOKIE_SAMESITE')
SESSION_COOKIE_NAME= environ.get('SESSION_COOKIE_NAME')