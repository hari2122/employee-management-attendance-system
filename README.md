# Employee Management & Attendance System

Python + SQL portfolio project for managing employee records, daily attendance, and leave requests using a Flask REST backend and MySQL database.

## Tech Stack
- Python
- Flask
- SQL / MySQL
- REST API
- Git

## Features
- Create, list, update, and delete employee records
- Mark daily attendance as PRESENT, ABSENT, or LEAVE
- Store check-in and check-out times
- Submit leave requests with PENDING status
- Retrieve employee attendance history
- Generate an attendance summary using SQL aggregation
- Relational schema with primary keys, foreign keys, unique constraints, and parameterized queries

## Setup
1. Run `sql/schema.sql` in MySQL.
2. Optionally run `sql/sample_data.sql`.
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and enter your MySQL credentials.
5. Start the application:
   ```bash
   python run.py
   ```
6. Verify with `GET http://localhost:5000/health`.

## API Endpoints
- `GET /api/employees`
- `POST /api/employees`
- `PUT /api/employees/<id>`
- `DELETE /api/employees/<id>`
- `POST /api/attendance`
- `GET /api/attendance/<employee_id>`
- `POST /api/leaves`
- `GET /api/reports/attendance-summary`

## Resume Alignment
**Employee Management & Attendance System | Python, SQL, MySQL, Git**

- Developed an employee management and attendance system using Python and MySQL to manage employee records, attendance, and leave information.
- Designed a MySQL relational database and used SQL queries to perform CRUD operations, including adding, retrieving, updating, and deleting employee records.

## Interview Topics
Review Python functions, Flask routes, CRUD, HTTP methods/status codes, MySQL joins, GROUP BY, primary/foreign keys, SQL constraints, parameterized queries, and database relationships before presenting the project.
