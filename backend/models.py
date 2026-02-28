from . import db 
from datetime import datetime 
from flask_security import UserMixin, RoleMixin 

# ROLES TABLE / ASSOCIATION db.Table
role_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), # Capital 'C'
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# 00. Role Model :-
class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(80),unique=True)
    description=db.Column(db.String(255))



# ==========================================
# 1. USER MODEL (The Core Identity)
# ==========================================
class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False) 

    #relationships 
    roles = db.relationship('Role', secondary = role_users, backref=db.backref('users', lazy='dynamic'))
    doctor = db.relationship('Doctor', back_populates = 'user', uselist=False)
    patient = db.relationship('Patient', back_populates='user', uselist=False)

    def to_dict(self):
        return{
            "id":self.id,
            "email":self.email,
            "role":[r.name for r in self.roles] #return list of roles for Vue 
        } 
    


# ==========================================
# 2. DOCTOR MODEL
# ========================================== 
class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) 
    career_start_year = db.Column(db.Integer, nullable=True)
    #foreign keys :-
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    #relationships : 
    user = db.relationship('User', back_populates='doctor')
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete")
    availabilities = db.relationship('DocAvailability', back_populates='doctor', cascade="all, delete-orphan") 
    
    @property 
    def experience(self):
        current_year = datetime.now().year

        if self.career_start_year:
            return current_year-self.career_start_year 
        return 0 
    
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "career_start_year": self.career_start_year,
            "email": self.user.email if self.user else None
        }



# ==========================================
# 3. PATIENT MODEL
# ========================================== 
class Patient(db.Model):
    __tablename__='patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    # Relationships
    user = db.relationship('User', back_populates='patient')
    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete") 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "email": self.user.email
        } 
    


# ==========================================
# 4. APPOINTMENT MODEL
# ==========================================  
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Booked") 
    #relationships
    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')
    treatment=db.relationship('Treatment', back_populates='appointment', uselist=False, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "doctor_name": self.doctor.name,
            "patient_name": self.patient.name,
            "date": self.appointment_datetime.isoformat(),
            "status": self.status
        } 



# ==========================================
# 5. TREATMENT MODEL
# ========================================== 
class Treatment(db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)

    diagnosis = db.Column(db.String(500), nullable=False)
    prescription = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    #relationships 
    appointment = db.relationship('Appointment', back_populates='treatment') 

    def to_dict(self):
        return {
            "id": self.id,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "appointment_id": self.appointment_id
        }
    


# ==========================================
# 6. DEPARTMENT MODEL
# ========================================== 
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  

    #One Department -> Many Doctors 
    doctors = db.relationship('Doctor', back_populates='department') 

    def to_dict(self):
        return{
            "id" : self.id, 
            "name" : self.name, 
            "doctor_count":len(self.doctors)
        } 
    


# ==========================================
# 7. DOCTOR AVAILABILITY MODEL
# ========================================== 
class DocAvailability(db.Model):
    __tablename__ = 'doc_availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)

    doctor = db.relationship('Doctor', back_populates='availabilities') 

    def to_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "start": self.start_time.isoformat() if self.start_time else None,
            "end": self.end_time.isoformat() if self.end_time else None,
            "is_booked": self.is_booked
        } 