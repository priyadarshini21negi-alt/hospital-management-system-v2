from datetime import datetime
from flask import current_app, request, jsonify
from flask_restful import Resource, Api
from flask_security import auth_required, current_user, hash_password
from .models import db, User, Patient, Doctor, Department, Appointment
from sqlalchemy import or_, and_ 


#---------------------------------------------
# 1. PATIENT REGISTRATION API (and admin managing patients)
#---------------------------------------------

class PatientRegister(Resource):
    def post(self):
       
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        number = data.get('number')
        
        #validation :-
        if not email or not password or not name:
            return{"message": "Email, Password, and Name are required"}, 400

        if User.query.filter_by(email=email).first():
            return{"message": "User with this email already exists"}, 409
        
        # flask-security datastore 
        ds = current_app.extensions['security'].datastore 

        try:
            #creating base user
            user = ds.create_user(
                email=email,
                password=hash_password(password),
                roles=['patient']
            )

            #creating patient profile one-one link
            patient = Patient(name=name, number=number, user=user)
            db.session.add(patient)
            db.session.commit()
            return {"message":"Patient registered successfully", "email":email}, 201 
        except Exception as e:
            db.session.rollback()
            return {"message":f"Registration failed: {str(e)}"}, 500


#--------------------------------------------------        
# 2. USER INFO API (For Frontend Redirects)
#------------------------------------------------------
class UserResource(Resource):
    @auth_required("token")
    def get(self):
        
        #Used by Vue.js to check if the token is valid and get the user's role.
        return {
            "id": current_user.id,
            "email": current_user.email,
            "roles": [r.name for r in current_user.roles],
            "active": current_user.active
        }
    

#--------------------------------------------------        
# 3. DOCTOR API (Public and Private)
#----------------------------------------------------
class DoctorAPI(Resource):
    #R : fetching all/one doc 
    @auth_required("token")
    def get(self, doctor_id=None):
        if doctor_id:
            doctor=Doctor.query.get(doctor_id)
            if not doctor:
                return {"message":"Doctor not found"}, 404 
            return doctor.to_dict(), 200 
        
            ''' milestone-03 A-D-M : Search Docs (by name/specialization)'''
        else:
            search_query = request.args.get('search','').strip()
            if search_query:
                doctors = Doctor.query.filter(
                    or_(
                        Doctor.name.ilike(f"%{search_query}%"),
                        Doctor.department.has(
                            Department.name.ilike(f"%{search_query}%")
                        )
                    )
                ).all()
            else:
                doctors=Doctor.query.all()
            return [doc.to_dict() for doc in doctors],200
        
    #C : admin adding new doc 
    @auth_required("token")
    def post(self):
        # SECURITY CHECK: Only Admin can add doctors
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized. Only admins can add doctors."}, 403

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')            
        name = data.get('name')
        department_id = data.get('department_id')
        career_start_year = data.get('career_start_year')

        if not email or not password or not name:
            return {"message": "Missing required fields"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 409

        ds = current_app.extensions['security'].datastore

        try:
            user = ds.create_user(email=email, password=hash_password(password), roles=['doctor']) 

            doctor = Doctor(name=name, 
                            user=user,
                            department_id=department_id, 
                            career_start_year=career_start_year
                            ) # Add specialization=data.get('specialization') if you have it
            db.session.add(doctor)
            db.session.commit()
            return {"message": "Doctor created successfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500 
        
    #U: admin update doc info 
    @auth_required("token")
    def put(self, doctor_id):
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized."}, 403
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404 
        
        data = request.get_json() 
        
        #updating:
        if 'name' in data:
            doctor.name = data['name']
        if 'department_id' in data:
            doctor.department_id = data['department_id']
        if 'career_start_year' in data:
            doctor.career_start_year = data['career_start_year'] 

        try:
            db.session.commit()
            return {"message": "Doctor updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
    #D : admin removing doc 

    @auth_required("token")
    def delete(self, doctor_id):
        # SECURITY CHECK: Only Admin can delete doctors
            if 'admin' not in [role.name for role in current_user.roles]:
                return {"message": "Unauthorized."}, 403

            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {"message": "Doctor not found"}, 404

            try:
                user = doctor.user
                db.session.delete(doctor)
                db.session.delete(user)
                db.session.commit()
                return {"message": "Doctor deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 500
            


#--------------------------------------------------        
# 4. PATIENT API (For Admin Dashboard)
#----------------------------------------------------
class PatientAPI(Resource):
    
    # R: Admin fetching all patients (with Search)
    @auth_required("token")
    def get(self):
        # SECURITY CHECK: Only Admin can view all patients
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized. Only admins can view patients."}, 403
            
        search_query = request.args.get('search', '').strip()
        
        if search_query:
            # Filter by Name OR cast ID to String for partial match search
            patients = Patient.query.filter(
                or_(
                    Patient.name.ilike(f"%{search_query}%"),
                    Patient.id.cast(db.String).ilike(f"%{search_query}%")
                )
            ).all()
        else:
            patients = Patient.query.all()
        
        # Serialize the data for Vue
        patient_list = []
        for p in patients:
            patient_list.append({
                "id": p.id,
                "name": p.name,
                "number": p.number
            })
            
        return patient_list, 200

    # D: Admin deleting a patient
    @auth_required("token")
    def delete(self, patient_id):
        # SECURITY CHECK: Only Admin can delete patients
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized."}, 403

        patient = Patient.query.get(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        try:
            # Hard delete: remove both patient profile and their login credentials
            user = patient.user
            db.session.delete(patient)
            if user:
                db.session.delete(user)
                
            db.session.commit()
            return {"message": "Patient deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
                

#--------------------------------------------------        
# 5. ADMIN APPOINTMENT API 
#---------------------------------------------------- 
class AdminAppointmentAPI(Resource):
    #fetching all appointment with search and filters 
    @auth_required("token")
    def get(self):
        if not any(role.name == "admin" for role in current_user.roles):
            return {"message": "Unauthorized."}, 403

        query = Appointment.query.join(Doctor).join(Patient) # Join early for search logic
        
        search_query = request.args.get('search', '').strip()
        if search_query:
            query = query.filter(
                or_(
                    Doctor.name.ilike(f"%{search_query}%"),
                    Patient.name.ilike(f"%{search_query}%"),
                    Appointment.status.ilike(f"%{search_query}%")
                )
            )

        category = request.args.get("category")
        now = datetime.utcnow()
        
        if category == "upcoming":
            query = query.filter(Appointment.appointment_datetime >= now) # Fixed typo
        elif category == "past":
            query = query.filter(Appointment.appointment_datetime < now) # Added logic
            
        appointments = query.order_by(Appointment.appointment_datetime.desc()).all()
        return [app.to_dict() for app in appointments], 200

    # U: Update appointment status (e.g., Cancelled)
    @auth_required("token")
    def put(self, appointment_id):
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized."}, 403
            
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404
            
        data = request.get_json()
        if 'status' in data:
            appointment.status = data['status']
            
        try:
            db.session.commit()
            return {"message": "Appointment updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

    # D: Delete an appointment entirely
    @auth_required("token")
    def delete(self, appointment_id):
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized."}, 403
            
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404
            
        try:
            db.session.delete(appointment)
            db.session.commit()
            return {"message": "Appointment deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

class AdminStatsAPI(Resource):
    @auth_required("token")
    def get(self):
        # Security check
        if 'admin' not in [role.name for role in current_user.roles]:
            return {"message": "Unauthorized. Admin access only."}, 403
            
        return {
            "total_patients": Patient.query.count(),
            "total_doctors": Doctor.query.count(),
            "total_appointments": Appointment.query.count()
        }, 200