from backend import create_app, db
from backend.models import User, Role
from flask_security import SQLAlchemyUserDatastore, hash_password

app = create_app()

def seed_data():
    with app.app_context():
        
        #creating all tables
        db.create_all()

        #initializing datastore
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)

        #creating roles
        admin_role = user_datastore.find_or_create_role(name='admin', description='System Administrator')
        doctor_role = user_datastore.find_or_create_role(name='doctor', description='Medical Professional')
        patient_role = user_datastore.find_or_create_role(name='patient', description='Hospital Patient')

        # create the Admin User
        if not user_datastore.find_user(email="admin@hms.com"):
            print("Creating Admin user...")
            user_datastore.create_user(
                email="admin@hms.com",
                password=hash_password("admin123"), # Hashes using bcrypt + salt from config
                roles=[admin_role]
            )
        else:
            print("Admin user already exists.")

       
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()