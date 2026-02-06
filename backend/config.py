#THE BRAIN 
import os 

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'hospital_v2.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security-Too (Token-Based auth)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SECURITY_PASSWORD_SALT = "salt-for-tokens"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    # Disabling session-based authentication 
    SECURITY_TOKEN_MAX_AGE = 3600 # 1 hour
    SECURITY_FLASH_MESSAGES = False 

    # CORS
    CORS_HEADERS = 'Content-Type'