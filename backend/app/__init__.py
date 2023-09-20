from flask import Flask
from flask_cors import CORS
from app.models import db, init_db
from flask_session import Session


def cors(app):
    # Apply CORS to the app
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


def create_app():
    
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    
    # Initialize the database
    init_db(app)

    # Apply CORS to the app using a separate function
    cors(app)
    
    Session(app)
    
    from app import routes
    # <app instence>.register_blueprint(<file name contains the blueprint>.<blue print name>)
    app.register_blueprint(routes.appRoutes)
        
    return app

