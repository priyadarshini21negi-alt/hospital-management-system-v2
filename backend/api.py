from flask import current_app, request, jsonify
from flask_restful import Resource, Api
from flask_security import auth_required, current_user, hash_password
from .models import db, User, Patient, Doctor

#---------------------------------------------
# 1. PATIENT REGISTRATION API
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
        
        #access the flask-security datastore 
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
                
        