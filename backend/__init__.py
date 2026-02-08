from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Api
from flask_cors import CORS

from .config import Config

db = SQLAlchemy()
security = Security()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    CORS(app)
    api = Api(app)

    # Security
    from .models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # API
    from .api import DoctorAPI, PatientRegister, UserResource
    
    api.add_resource(DoctorAPI,
                     '/api/doctors',
                     '/api/doctors/<int:doctor_id>')
   
    api.add_resource(PatientRegister,
                     '/api/register',
                    )
  
    api.add_resource(UserResource,
                     '/api/user_info',
                    )

    # DB tables
    with app.app_context():
        db.create_all()

    return app


