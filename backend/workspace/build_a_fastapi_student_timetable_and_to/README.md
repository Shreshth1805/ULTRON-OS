# Student Timetable and Todo List Scheduler API
This API provides a simple and efficient way to manage student timetables and todo lists. It uses FastAPI as the web framework and JWT for authentication.

## Features
* User registration and login
* JWT authentication
* Create, read, update and delete student timetables
* Create, read, update and delete todo lists
* Assign todo lists to student timetables

## Requirements
* Python 3.8+
* FastAPI
* Uvicorn
* Pydantic
* JWT
* SQLAlchemy
* PostgreSQL

## Installation
pip install fastapi uvicorn pydantic jwt sqlalchemy psycopg2

## Usage
uvicorn main:app --host 0.0.0.0 --port 8000

## API Endpoints
### Authentication
* POST /register - Register a new user
* POST /login - Login a user

### Student Timetables
* GET /timetables - Get all student timetables
* GET /timetables/{timetable_id} - Get a student timetable by id
* POST /timetables - Create a new student timetable
* PUT /timetables/{timetable_id} - Update a student timetable
* DELETE /timetables/{timetable_id} - Delete a student timetable

### Todo Lists
* GET /todo - Get all todo lists
* GET /todo/{todo_id} - Get a todo list by id
* POST /todo - Create a new todo list
* PUT /todo/{todo_id} - Update a todo list
* DELETE /todo/{todo_id} - Delete a todo list

### Assign Todo Lists to Student Timetables
* POST /timetables/{timetable_id}/todo - Assign a todo list to a student timetable
* DELETE /timetables/{timetable_id}/todo/{todo_id} - Unassign a todo list from a student timetable

## Example Use Cases
* Register a new user: curl -X POST -H "Content-Type: application/json" -d '{"username": "john", "password": "hello"}' http://localhost:8000/register
* Login a user: curl -X POST -H "Content-Type: application/json" -d '{"username": "john", "password": "hello"}' http://localhost:8000/login
* Create a new student timetable: curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Math", "time": "10:00"}' http://localhost:8000/timetables
* Create a new todo list: curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Homework", "due_date": "2024-03-16"}' http://localhost:8000/todo
* Assign a todo list to a student timetable: curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"todo_id": 1}' http://localhost:8000/timetables/1/todo