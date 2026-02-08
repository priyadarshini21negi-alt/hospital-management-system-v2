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
    def get(self, doctor_id = None):
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {"message": "Doctor not found"}, 404
            return doctor.to_dict(), 200
        else:
            doctors = Doctor.query.all()
            return [doc.to_dict() for doc in doctors], 200