<h1>Hospital Management System V2 (HMS-V2)</h1>
<h2>Overview</h2>
<p>HMS-V2 is an hospital management platform designed to streamline interactions between <b>Admins, Doctors, and Patients.</b> This project is a scalable upgrade of the MAD 1 architecture, transitioning from a monolith to a modern decoupled architecture with a dedicated API backend and a reactive frontend.</p>
<br>
<h2>Tech Stack</h2>
<ul>
<li><b>Frontend:</b> Vue.js 3, Vue Router, Vuex/Pinia, Bootstrap 5 </li>
<li><b>Backend:</b> Python, Flask, Flask-RESTful</li>
<li><b>Database:</b> SQLite (via SQLAlchemy)</li>
<li><b>Authentication:</b> Token-based (JWT)</li>
<li><b>Async Tasks:</b> Celery & Redis</li>
<li><b>Caching:</b> Flask-Caching (Redis)</li>
</ul>
<br>
<h2>Key Features</h2>
<ul>
<li><b>Role-Based Dashboards:</b> Unique interfaces for Admin (system control), Doctor (patient/schedule management), and Patient (booking/records).</li>
<li><b>Asynchronous Processing:</b> Daily reminders and monthly report generation via Celery.</li>
<li><b>Performance Optimization:</b> Caching of frequently accessed data like department lists and doctor profiles.</li>
<li><b>Secure APIs:</b> Token-based access to ensure data privacy across all endpoints.</li>
</ul>
<br>
