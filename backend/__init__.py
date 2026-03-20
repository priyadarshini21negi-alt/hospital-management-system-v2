from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Api
from flask_cors import CORS
from .config import Config
from datetime import datetime, timedelta

from celery import Celery 
from celery.schedules import crontab 

db = SQLAlchemy()
security = Security()
celery = Celery(__name__, 
                broker="redis://localhost:6379/0",
                backend="redis://localhost:6379/0")
@celery.task 
def generate_monthly_reports():
    from .models import Doctor, Appointment 
    #importing inside cuz it was crashing in Circular imports 

    print("Generating monthly reports for all doctors...")

    #prev 30 days :-
    end_date=datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    month_str = end_date.strftime("%B %Y")

    doctors = Doctor.query.all()
    for doc in doctors :
        #fetching only completed appointments 
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doc.id,
            Appointment.status=="Completed",
            Appointment.appointment_datetime >= start_date,
            Appointment.appointment_datetime<=end_date
        ).all()

        #rendering html template with data 
        html_content = render_template('monthly_report.html',
        doctor = doc, appointments=appointments, month=month_str)

        file_name=f"report_doc_{doc.id}_{month_str.replace(' ','_')}.html"
        with open(file_name, "w") as f:
            f.write(html_content)

        print(f"Report generated for {doc.name}")
    return "All Monthly Reports Genereated."



@celery.task 
def send_daily_reminders():
    print("Sending patient reminders")
    return "Reminders Sent"

celery.conf.beat_schedule = {
    'test-reminders-every-minute': {
        'task': 'backend.send_daily_reminders',  
        'schedule': crontab(minute='*'),
    },
    'monthly-report-1st-day': {
        'task':'backend.generate_monthly_reports',
        'schedule':crontab(minute=0, hour=0, day_of_month=1),
        #'schedule':crontab(minute='*'), 
    }
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    celery.conf.update(app.config)

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


