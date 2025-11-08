# Teacher-Student Management System (Flask Web Application)

## Project Overview

This Flask web application implements a multi-role user management system with distinct logins for **Teachers**, **Students**, and an **Admin**. It supports:

- Registration and login for Teachers and Students.
- Admin approval of newly registered users.
- Viewing of approved Teachers by Students and vice versa.
- Role-based access control ensuring users access appropriate views.

This project demonstrates fundamental Flask concepts such as routing, template rendering, user roles, and approval workflows.

---

## Features

- **Separate Registration & Login** for Teachers and Students.
- **Admin Approval Panel** to review and approve or reject new registrations.
- **Mutual Visibility** where approved Teachers and Students can view each other's profiles.
- **Role-Based Access Control** to restrict pages and actions based on user type and approval status.

---

## Getting Started

### Prerequisites

- Python 3.x
- Flask (installable via pip)
- Recommended: virtual environment (venv)

### Installation

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
Create and activate a virtual environment (recommended):

bash
Copy code
python -m venv env
# Activate on Windows:
env\Scripts\activate
# Activate on Linux/macOS:
source env/bin/activate
Install dependencies from requirements.txt:

bash
Copy code
pip install -r requirements.txt
Running the Application
Start the Flask development server:

bash
Copy code
flask run
Or, if your main app file is app.py, run:

bash
Copy code
python app.py
Open your browser and visit:

http://localhost:5000/ — Main landing page and login

Application Workflow
Registration
Teachers and Students can register via separate forms.

New accounts are marked pending until approved by Admin.

Admin Panel
Admin logs in with predefined credentials.

Views all pending registrations (Teachers and Students).

Can approve or reject accounts.

Approved users gain access to dashboards.

Approved User Interaction
Approved Students can view a list of approved Teachers.

Approved Teachers can view a list of approved Students.

Admin Credentials :
Username: admin
Password: admin

Security Notice: Change the admin credentials in production to secure your application.
