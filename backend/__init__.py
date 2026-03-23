from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Api
from flask_cors import CORS
from .config import Config
from datetime import datetime, timedelta

from flask_mail import Mail, Message
from flask_caching import Cache 

from celery import Celery 
from celery.schedules import crontab 

import csv 
import os 


db = SQLAlchemy()
cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300 # Default TTL is 5 minutes
})
security = Security()
mail = Mail()
celery = Celery(__name__, 
                broker="redis://localhost:6379/0",
                backend="redis://localhost:6379/0")

@celery.task(name="backend.export_patient_history")
def export_patient_history(patient_id):
    from .models import Appointment, Patient 
    from flask import current_app 

    print(f"Starting CSV export for Patient ID: {patient_id}")

    patient = Patient.query.get(patient_id)
    if not patient:
        return "patient not found."

    history = Appointment.query.filter_by(
        patient_id=patient_id,
        status="completed"
    ).order_by(Appointment.appointment_datetime.desc()).all() 

    #ensuring export directory exists 
    export_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    file_name=f"patient_{patient_id}_history.csv"
    file_path=os.path.join(export_dir, file_name) 

    #writing the csv file 
    with open(file_path,'w',newline='') as csvfile:
        fieldnames = ['Date', 'Doctor', 'Diagnosis', 'Prescription', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 

        writer.writeheader()
        for app in history:
            writer.writerow({
                'Date': app.appointment_datetime.strftime("%Y-%m-%d %H:%M"),
                'Doctor': app.doctor.name if app.doctor else 'N/A',
                'Diagnosis': app.treatment.diagnosis if app.treatment else 'N/A',
                'Prescription': app.treatment.prescription if app.treatment else 'N/A',
                'Notes': app.treatment.notes if app.treatment else ''
            })
    #email alert sending 
    msg = Message(
        subject = "Your medical history is ready",
        sender="noreply@healix.com",
        recipients=[patient.user.email]
    )
    msg.body = f"Hello {patient.name},\n\nYour requested medical history export has been generated successfully.\n\nHealix Hospital"
    mail.send(msg)

    print(f"Export complete. File saved at {file_path}")
    return file_path



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


#
@celery.task 
def send_daily_reminders():
    from .models import Appointment 
    from flask import current_app 

    print("Starting Daily Reminders Job...")
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1) 

    todays_appointments = Appointment.query.filter(
        Appointment.status == "Booked",
        Appointment.appointment_datetime >= today_start,
        Appointment.appointment_datetime < today_end
    ).all()
    if not todays_appointments:
        print("No reminders to send today.")
        return "No reminders to send today."

    for app in todays_appointments:
        patient_email = app.patient.user.email
        doctor_name = app.doctor.name
        time_str = app.appointment_datetime.strftime("%I:%M %p")

        msg = Message(
            subject=f"Reminder: Appointment with {doctor_name} Today",
            sender="noreply@healix.com",
            recipients=[patient_email]
        )
       
        msg.body = f"Hello {app.patient.name},\n\nThis is a reminder that you have an appointment scheduled with {doctor_name} today at {time_str}.\n\nPlease arrive 10 minutes early.\n\nThank you,\nHealix Hospital"
        mail.send(msg)
        print(f"Reminder sent to {patient_email}")
    return f"Sent {len(todays_appointments)} reminders."

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
    mail.init_app(app)

    #cache 
    cache.init_app(app)

    # Security
    from .models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # API
    
    from .api import DoctorAPI, PatientRegister, UserResource, PatientAPI, AdminAppointmentAPI, AdminStatsAPI, DoctorAppointmentsAPI, PatientAppointmentsAPI, DocAvailabilityAPI, PatientProfileAPI 
    from .api import DoctorPublicSlotsAPI, DoctorPatientHistoryAPI
    from .api import ExportHistoryAPI
    
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

    #celery tasks : 
    api.add_resource(ExportHistoryAPI, '/api/patient/export')

  

    # DB tables
    with app.app_context():
        db.create_all()

    return app


