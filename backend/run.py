from app import create_app

app = create_app()



if __name__ == '__main__':
    app.run()
    
    """
backend/
    app/
        __init__.py
        config.py 
        models.py  
        routes.py
        helpers.py
    instance/
        mydatabase.db
    .env
    .flaskenv
    run.py
frontend/
puplic/
src/
    """