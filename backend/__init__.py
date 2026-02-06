from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from .config import Config 

db = SQLAlchemy()
security = Security()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    #setting up Flask-Security 
    from .models import User, Role 
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore) 
    return app 
