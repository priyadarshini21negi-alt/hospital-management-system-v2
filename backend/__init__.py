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
    
    from .api import DoctorAPI, PatientRegister, UserResource, PatientAPI, AdminAppointmentAPI, AdminStatsAPI, DoctorAppointmentsAPI, PatientAppointmentsAPI, DocAvailabilityAPI, PatientProfileAPI 
    from .api import DoctorPublicSlotsAPI, DoctorPatientHistoryAPI
    
    api.add_resource(DoctorAPI,
                     '/api/doctors',
                     '/api/doctors/<int:doctor_id>')
   
    api.add_resource(PatientRegister,
                     '/api/register',
                    )
  
    api.add_resource(UserResource,
                     '/api/user_info',
                    )
    api.add_resource(AdminStatsAPI, '/api/admin/stats')

    # PATIENTS :- 
    api.add_resource(PatientAPI,
                     '/api/patients',
                     '/api/patients/<int:patient_id>'
                    )
    api.add_resource(AdminAppointmentAPI,
                     '/api/admin/appointments',
                     '/api/admin/appointments/<int:appointment_id>'
                    )
    
    api.add_resource(PatientAppointmentsAPI, '/api/patient/appointments',
                    '/api/patient/appointments',
                    '/api/patient/appointments/<int:appointment_id>' )
    

    api.add_resource(PatientProfileAPI, '/api/patient/profile')

    api.add_resource(DoctorPublicSlotsAPI, '/api/doctors/<int:doctor_id>/slots')

    #doctors 
    api.add_resource(DoctorAppointmentsAPI, '/api/doctor/appointments',
                     '/api/doctor/appointments',
                     '/api/doctor/appointments/<int:appointment_id>')

    api.add_resource(DocAvailabilityAPI, 
                 '/api/doctor/availability', 
                 '/api/doctor/availability/<int:slot_id>')
    
    api.add_resource(DoctorPatientHistoryAPI, '/api/doctor/patient/<int:patient_id>/history')

    # DB tables
    with app.app_context():
        db.create_all()

    return app


