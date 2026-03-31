# Hospital Management System V2 (HMS-V2)

## Overview
HMS-V2 is a hospital management platform designed to streamline interactions between **Admins, Doctors, and Patients**. This project is a scalable upgrade of the MAD 1 architecture, transitioning from a monolith to a modern decoupled architecture with a dedicated API backend and a reactive frontend.

## Tech Stack
* **Frontend:** Vue.js 3, Vue Router, Vuex/Pinia, Bootstrap 5 
* **Backend:** Python, Flask, Flask-RESTful
* **Database:** SQLite (via SQLAlchemy)
* **Authentication:** Token-based (JWT)
* **Async Tasks:** Celery & Redis
* **Caching:** Flask-Caching (Redis)

## Key Features
* **Role-Based Dashboards:** Unique interfaces for Admin (system control), Doctor (patient/schedule management), and Patient (booking/records).
* **Asynchronous Processing:** Daily reminders and monthly report generation via Celery.
* **Performance Optimization:** Caching of frequently accessed data like department lists and doctor profiles.
* **Secure APIs:** Token-based access to ensure data privacy across all endpoints.

## How to Run the Application

**Step 1: Start Redis (Background Service)**
`sudo service redis-server start`

**Step 2: Start the Flask Backend (Terminal 1)**
`source venv/bin/activate`
`python3 -m backend.app`

**Step 3: Start the Vue Frontend (Terminal 2)**
`cd frontend`
`npm run serve`

**Step 4: Start the Celery Worker (Terminal 3)**
`source venv/bin/activate`
`celery -A celery_worker.celery worker --loglevel=info`

**Step 5: Start the Celery Beat Scheduler (Terminal 4)**
`source venv/bin/activate`
`celery -A celery_worker.celery beat --loglevel=info`