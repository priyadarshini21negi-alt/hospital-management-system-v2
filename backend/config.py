import os 

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'hospital_v2.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security-Too settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SECURITY_PASSWORD_SALT = "salt-for-tokens"
    SECURITY_PASSWORD_HASH = "bcrypt" # Required for security
    
    # Token-Based Auth
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_MAX_AGE = 3600 
    SECURITY_FLASH_MESSAGES = False 
    WTF_CSRF_ENABLED = False # CRITICAL: Disable for pure APIs

    # --- CRITICAL FIX FOR API LOGIN ---
    WTF_CSRF_ENABLED = False                        # 1. Disable Flask-WTF CSRF
    SECURITY_CSRF_PROTECT_MECHANISMS = []           # 2. Disable Security CSRF mechanisms
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True    # 3. Allow login without CSRF
    # ----------------------------------

    # CORS
    CORS_HEADERS = 'Content-Type'