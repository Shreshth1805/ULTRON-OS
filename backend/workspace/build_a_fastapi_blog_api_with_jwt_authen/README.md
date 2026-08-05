# FastAPI Blog API with JWT Authentication
This is a FastAPI application that provides a RESTful API for managing blog posts, with JWT authentication for secure user management.

## Features
* User registration and login with JWT authentication
* Create, read, update, and delete blog posts
* Authentication and authorization for protected routes

## Requirements
* Python 3.8+
* FastAPI 0.92.0+
* uvicorn 0.18.2+
* python-jose 3.3.0+
* passlib 1.9.0+

## Installation
To install the required dependencies, run the following command:
pip install fastapi uvicorn python-jose passlib

## Usage
To start the application, run the following command:
uvicorn main:app --host 0.0.0.0 --port 8000

## API Endpoints
The following endpoints are available:
* POST /register: Register a new user
* POST /login: Login an existing user
* GET /posts: Get all blog posts
* GET /posts/{post_id}: Get a single blog post
* POST /posts: Create a new blog post
* PUT /posts/{post_id}: Update a blog post
* DELETE /posts/{post_id}: Delete a blog post

## Example Use Cases
* Register a new user: curl -X POST -H "Content-Type: application/json" -d '{"username": "john", "password": "hello"}' http://localhost:8000/register
* Login an existing user: curl -X POST -H "Content-Type: application/json" -d '{"username": "john", "password": "hello"}' http://localhost:8000/login
* Get all blog posts: curl -X GET http://localhost:8000/posts
* Create a new blog post: curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"title": "Hello World", "content": "This is a sample blog post"}' http://localhost:8000/posts