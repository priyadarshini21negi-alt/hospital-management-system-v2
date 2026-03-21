import os 

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'hospital_v2.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security-Too settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SECURITY_PASSWORD_SALT = "salt-for-tokens"
    SECURITY_PASSWORD_HASH = "bcrypt" 
    
    # Token-Based Auth
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_MAX_AGE = 3600 
    SECURITY_FLASH_MESSAGES = False 
    WTF_CSRF_ENABLED = False 

    WTF_CSRF_ENABLED = False                       
    SECURITY_CSRF_PROTECT_MECHANISMS = []           
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True    
    # ----------------------------------

    # CORS
    CORS_HEADERS = 'Content-Type'


    #FLASK-MAIN (MailTrap for testing)
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '1f9dac9bcdeca1'
    MAIL_PASSWORD = '79ec67f721c176'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


   
