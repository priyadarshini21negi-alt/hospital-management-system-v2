from datetime import datetime, timedelta
from flask import current_app, request
from flask_restful import Resource
from functools import wraps
from flask_security import auth_required, current_user, hash_password
from .models import db, User, Patient, Doctor, Department, Appointment, Treatment, DocAvailability
from sqlalchemy import or_, and_ 
from sqlalchemy.exc import IntegrityError

from . import cache
import enum 



#--------------------------------------------
# ROLES / RBAC DECORATOR
#--------------------------------------------
def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not any(role.name == role_name for role in current_user.roles):
                return {"message": f"Unauthorized. {role_name.capitalize()} access required."}, 403
            
            return func(*args, **kwargs) 
        return wrapper
    return decorator

class AppointmentStatus(enum.Enum):
    BOOKED = "Booked"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

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
    @auth_required("token")

    def get(self, doctor_id=None):
        search_query = request.args.get('search', '').strip()

        if doctor_id:
            cache_key = f"doctors_list_{doctor_id}"
        else:
            cache_key = f"doctors_list_None_search_{search_query}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200 

        #---db fetch logic---
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {"message": "Doctor not found"}, 404 
            res = doctor.to_dict()
        else:
            if search_query:
                doctors=Doctor.query.filter(
                    or_(
                        Doctor.name.ilike(f"%{search_query}%"),
                        Doctor.department.has(Department.name.ilike(f"%{search_query}%"))
                    )
                ).all()
            else:
                doctors = Doctor.query.all()
            res = [doc.to_dict() for doc in doctors]

        # ---CACHING LOGIC ---
        cache.set(cache_key, res, timeout=300) 
        print(f"Cache Miss: Saved {cache_key} to Redis")
        return res, 200 
        
    @auth_required("token")
    @role_required("admin")
    def post(self):
        data = request.get_json()
        
        # --VALIDATION--
        ds = current_app.extensions['security'].datastore
        
        try:
            #creating base user
            user = ds.create_user(
                email=data.get('email'),
                password=hash_password(data.get('password')),
                roles = ['doctor']
            )

            #creating new doc and linking to user 
            new_doctor = Doctor(
                name=data.get('name'),
                career_start_year=data.get("career_start_year"),
                department_id = data.get('department_id'),
                user=user
            )


            db.session.add(new_doctor)
            db.session.commit()
           
            cache.delete("doctors_list_None_search_")
            return {"message": "Doctor created successfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500 

    @auth_required("token")
    @role_required("admin")
    def put(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404 

        data = request.get_json()
        try:
            # updating the fields 
            if 'name' in data:
                doctor.name = data['name']
            if 'career_start_year' in data:
                doctor.career_start_year = data['career_start_year']
            if 'department_id' in data:
                doctor.department_id = data['department_id']
            if 'email' in data:
                doctor.user.email = data['email']

            db.session.commit()
            
            cache.delete("doctors_list_None_search_")
            cache.delete(f"doctors_list_{doctor_id}")
            return {"message": "Doctor updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
       
        
    @auth_required("token")
    @role_required("admin")
    def delete(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        try:
            user = doctor.user
            db.session.delete(doctor)
            db.session.delete(user)
            db.session.commit()
          
            cache.delete("doctors_list_None_search_")
            cache.delete(f"doctors_list_{doctor_id}")
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
    @role_required("admin")
    def get(self):     
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
    @role_required("admin")
    def delete(self, patient_id):
        

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
    @role_required("admin")
    def get(self):
        

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
    @role_required("admin")
    def put(self, appointment_id):
      
            
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
    @role_required("admin")
    def delete(self, appointment_id):
        
            
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
    @role_required("admin")
    def get(self):
        # Security check
           
        return {
            "total_patients": Patient.query.count(),
            "total_doctors": Doctor.query.count(),
            "total_appointments": Appointment.query.count()
        }, 200


#--------------------------------------------------        
# 6. DOCTOR'S APPOINTMENT & TREATMENT API 
#---------------------------------------------------- 
class DoctorAppointmentsAPI(Resource):
    @auth_required("token")
    @role_required("doctor")
    def get(self):
  
        
        # specific doc - userprofile
        current_doctor = current_user.doctor 
        if not current_doctor:
            return {"message": "Doctor profile not found."}, 404

        #  ONLY this doctor's appointments
        appointments = Appointment.query.filter_by(doctor_id=current_doctor.id).order_by(Appointment.appointment_datetime.asc()).all()
        
        # Includes treatment info if completed
        result = []
        for app in appointments:
            app_data = app.to_dict()
            if app.treatment:
                app_data['treatment'] = app.treatment.to_dict()
            else:
                app_data['treatment'] = None
            result.append(app_data)
            
        return result, 200

    #  Add a treatment to an appointment
    @auth_required("token")
    @role_required("doctor")
    def post(self):
       

        data = request.get_json()
        appointment_id = data.get('appointment_id')
        
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {"message": "Appointment not found"}, 404
         # appointment actually belongs to this doctor
        if appointment.doctor_id != current_user.doctor.id:
            return {"message": "You cannot treat another doctor's patient."}, 403

        try:
            # Create Treatment
            new_treatment = Treatment(
                appointment_id=appointment.id,
                diagnosis=data.get('diagnosis'),
                prescription=data.get('prescription'),
                notes=data.get('notes', '')
            )
            # Update Appointment Status
            appointment.status = AppointmentStatus.COMPLETED.value 
            
            db.session.add(new_treatment)
            db.session.commit()
            return {"message": "Treatment added and appointment completed!"}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
    # D doc cancelling appointment 
    @auth_required("token")
    @role_required("doctor")
    def put(self, appointment_id=None):
        
            
        if not appointment_id:
            return {"message": "Appointment ID required"}, 400

        appointment = Appointment.query.get(appointment_id)
        
        #ensuring appointment exists and belongs to this doc 
        if not appointment or appointment.doctor_id != current_user.doctor.id:
            return {"message": "Appointment not found or unauthorized."}, 404 
        data = request.get_json()
        if data.get('status') == 'Cancelled':
            if appointment.status == 'Completed':
                return {"message": "Cannot cancel a completed consultation."}, 400
                
            appointment.status = AppointmentStatus.CANCELLED.value
            
            slot=DocAvailability.query.filter_by(
                doctor_id=appointment.doctor_id, 
                start_time=appointment.appointment_datetime
            ).first() 
            if slot:
                slot.is_booked = False 
            try:
                db.session.commit()
                return {"message": "Appointment cancelled successfully."}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 500
        return {"message": "Invalid status update"}, 400

#--------------------------------------------------        
# 7. PATIENT APPOINTMENT API 
#---------------------------------------------------- 
class PatientAppointmentsAPI(Resource):
    # R: Patient viewing their own appointments
    @auth_required("token")
    @role_required("patient")
    def get(self):
         
        appointments = Appointment.query.filter_by(
            patient_id=current_user.patient.id
        ).order_by(Appointment.appointment_datetime.asc()).all()
        
        result = []
        for app in appointments:
            app_data = app.to_dict()
            if app.treatment:
                app_data['treatment'] = app.treatment.to_dict()
            else:
                app_data['treatment'] = None
            result.append(app_data)
        return result, 200

    # C: Patient booking a new appointment
    @auth_required("token")
    @role_required("patient")
    def post(self):
        
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        datetime_str = data.get('appointment_datetime') # Expected: YYYY-MM-DDTHH:MM
        
        if not doctor_id or not datetime_str:
            return {"message": "Doctor and Date/Time are required"}, 400

        try: #post methods
            app_dt = datetime.fromisoformat(datetime_str)
            new_slot = DocAvailability.query.filter_by( doctor_id=doctor_id, start_time=app_dt).first()
            
            if not new_slot:
                return {"message": "This time slot does not exist."}, 404 
            if new_slot.is_booked:
                return {"message": "This slot is already booked!"}, 409 
            
            


            #--logic preventing patient overlap 
            active_appointments = Appointment.query.filter_by(
                patient_id=current_user.patient.id,
                status="Booked"
                ).all() 
            for app in active_appointments:
                existing_slot = DocAvailability.query.filter_by(
                    doctor_id=app.doctor_id,
                    start_time=app.appointment_datetime
                ).first()
                
                if existing_slot:
                    if existing_slot.start_time < new_slot.end_time and existing_slot.end_time > new_slot.start_time:
                        return {"message": f"Conflict! You already have an appointment with {app.doctor.name} at this time."}, 409 

            #if no overlap then go on with the booking 
            new_slot.is_booked = True        

            new_appointment = Appointment(
                patient_id=current_user.patient.id, 
                doctor_id=doctor_id,
                appointment_datetime=app_dt,
                status="Booked"
            )
            db.session.add(new_appointment)
            db.session.commit()

            cache.delete(f'/api/doctors/{doctor_id}/slots')

            return {"message": "Appointment booked successfully!"}, 201
            
        except IntegrityError:
            db.session.rollback()
            return {"message": "Too slow! This slot was just booked by someone else."}, 409
            
        except ValueError:
            return {"message": "Invalid date format."}, 400

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
    # D : Patient cancelling appointment 
    @auth_required("token")
    @role_required("patient")
    def delete(self, appointment_id=None):
       
        if not appointment_id:
            return {"message": "Appointment ID required"}, 400 
        
        #finding appointment and verifying ownership 
        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.patient_id != current_user.patient.id:
            return {"message": "Appointment not found or unauthorized."}, 404 
        #preventing cancelling past/completed appointment 
        if appointment.status==AppointmentStatus.COMPLETED.value:
            return {"message": "Cannot cancel a completed consultation."}, 400 
        
        try: 
            # unbooking on doc's side
            slot=DocAvailability.query.filter_by(
                doctor_id=appointment.doctor_id,
                start_time=appointment.appointment_datetime
            ).first() 

            if slot:
                slot.is_booked = False 

            
            db.session.delete(appointment)
            db.session.commit()

            
            cache.delete(f'/api/doctors/{appointment.doctor_id}/slots')

            return {"message": "Appointment cancelled successfully."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Database error : {str(e)}"}, 500
#--------------------------------------------------        
# 7. AVAILABLE SLOTS FOR PATIENT.
#----------------------------------------------------
class DoctorPublicSlotsAPI(Resource):
    @auth_required("token")
    
    
    def get(self, doctor_id): 
        now = datetime.utcnow() 
        slots = DocAvailability.query.filter(
            and_(
                DocAvailability.doctor_id==doctor_id,
                DocAvailability.start_time >= now,
                DocAvailability.is_booked == False   
            )
        ).order_by(DocAvailability.start_time.asc()).all()
        return [slot.to_dict() for slot in slots], 200



#--------------------------------------------------        
# 9. PATIENT UPDATE PROFILE API 
#---------------------------------------------------
class PatientProfileAPI(Resource):
    @auth_required("token")
    @role_required("patient")
    def get(self):
       

        patient = current_user.patient 
        return {
            "name": patient.name,
            "number": patient.number,
            "email": current_user.email
        }, 200 

    @auth_required("token")
    @role_required("patient")
    def put(self):
        
       

        data = request.get_json()
        patient = current_user.patient
        
        # Update fields if they were provided
        if 'name' in data:
            patient.name = data['name']
        if 'number' in data:
            patient.number = data['number']
            
        try:
            db.session.commit()
            return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500





#--------------------------------------------------        
# 8. DOCTOR AVAILABILITY API 
#---------------------------------------------------
class DocAvailabilityAPI(Resource):
    @auth_required("token")
    @role_required("doctor")
    def get(self):   #future available slots
       

        now = datetime.utcnow()
        slots = DocAvailability.query.filter(
            and_(
                DocAvailability.doctor_id == current_user.doctor.id, 
                DocAvailability.start_time >= now 
            )
        ).order_by(DocAvailability.start_time.asc()).all()

        return [slot.to_dict() for slot in slots], 200 


    @auth_required("token")
    @role_required("doctor")
    def post(self):

        try:
            data = request.get_json()

            start_dt = datetime.fromisoformat(data.get('start_time'))
            end_dt = datetime.fromisoformat(data.get('end_time'))

            now = datetime.utcnow()
            limit = now + timedelta(days=7)

            # Past Check
            if start_dt < now:
                return {"message": "Cannot schedule slots in the past."}, 400

            # 7 Day Limit
            if start_dt > limit:
                return {"message": "Availability can only be set for next 7 days."}, 400

            # End > Start
            if end_dt <= start_dt:
                return {"message": "End time must be after start time."}, 400

            # Overlap Check
            overlapping = DocAvailability.query.filter(
                DocAvailability.doctor_id == current_user.doctor.id,
                DocAvailability.start_time < end_dt,
                DocAvailability.end_time > start_dt
            ).first()

            if overlapping:
                return {"message": "This slot overlaps with an existing slot."}, 409

            # Create Slot
            new_slot = DocAvailability(
                doctor_id=current_user.doctor.id,
                start_time=start_dt,
                end_time=end_dt,
                is_booked=False
            )

            db.session.add(new_slot)
            db.session.commit()

        
            cache.delete(f'/api/doctors/{current_user.doctor.id}/slots')

            return {"message": "Availability added successfully!"}, 201

        except ValueError:
            return {"message": "Invalid date format."}, 400

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500


    # ---------------------------------------
    # DELETE SLOT
    # ---------------------------------------
    @auth_required("token")
    @role_required("doctor")
    def delete(self, slot_id):

       

        slot = DocAvailability.query.get(slot_id)

        if not slot or slot.doctor_id != current_user.doctor.id:
            return {"message": "Slot not found or unauthorized."}, 404 

        if slot.is_booked:
            return {"message": "Cannot delete a booked slot."}, 400 

        try:
            db.session.delete(slot)
            db.session.commit()

          
            cache.delete(f'/api/doctors/{current_user.doctor.id}/slots')

            return {"message": "Slot removed."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
#--------------------------------------------------        
# 10. DOCTOR VIEWING PATIENT HISTORY API
#---------------------------------------------------
class DoctorPatientHistoryAPI(Resource):
    @auth_required("token")
    @role_required("doctor")
    def get(self, patient_id):
        
        
        history = Appointment.query.filter_by(
            patient_id=patient_id,
            doctor_id=current_user.doctor.id,
            status=AppointmentStatus.COMPLETED.value 
        ).order_by(Appointment.appointment_datetime.desc()).all() 

        result=[]
        for app in history:
            app_data=app.to_dict()
            if app.treatment:
                app_data['treatment'] = app.treatment.to_dict()
            result.append(app_data)
        return result, 200


#--------------------------------------------------        
# 11. ASYNC CSV EXPORT API
#---------------------------------------------------
class ExportHistoryAPI(Resource):
    @auth_required("token")
    @role_required("patient")
    def post(self):
         
        patient_id = current_user.patient.id 

        #importing task here to avoid circular imports 
        from .__init__ import export_patient_history 
        #triggering the celery task asynchronously using .delay()
        task =  export_patient_history.delay(patient_id)
        # Return immediately to the user while Celery works in the background
        return {
            "message":"Export Started.",
            "task_id":task.id 
        }, 202