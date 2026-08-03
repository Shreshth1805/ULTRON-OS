FastAPI Blog API
This is a FastAPI CRUD blog API using SQLite and SQLAlchemy.
It provides endpoints for creating, reading, updating, and deleting blog posts.
The API uses Pydantic for schema validation and SQLAlchemy for database operations.
To run the API, use the command uvicorn main:app --host 0.0.0.0 --port 8000.
You can test the API endpoints using a tool like curl or a REST client.
The API has the following endpoints:
- POST /blogs/ : Create a new blog post
- GET /blogs/ : Get all blog posts
- GET /blogs/{blog_id} : Get a blog post by id
- PUT /blogs/{blog_id} : Update a blog post
- DELETE /blogs/{blog_id} : Delete a blog post
The API uses a SQLite database and stores the blog posts in a table called blogs.
The blog posts have the following fields:
- id : A unique identifier for the blog post
- title : The title of the blog post
- content : The content of the blog post
- created_at : The date and time the blog post was created