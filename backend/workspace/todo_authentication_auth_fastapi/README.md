# TodoApp README

## Introduction
TodoApp is a simple FastAPI todo application with authentication and SQLite database. This application allows users to create, read, update, and delete (CRUD) todo items.

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Installation
To install the required dependencies, run the following command:
```bash
pip install -r requirements/prod.txt
```

## Running the Application
To run the application, use the following command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints
The following API endpoints are available:
- **POST /users**: Create a new user
- **POST /login**: Login to the application
- **GET /todos**: Get all todo items
- **POST /todos**: Create a new todo item
- **GET /todos/{todo_id}**: Get a todo item by ID
- **PUT /todos/{todo_id}**: Update a todo item
- **DELETE /todos/{todo_id}**: Delete a todo item

## Docker
To build the Docker image, run the following command:
```bash
docker build -t todoapp .
```
To run the Docker container, use the following command:
```bash
docker run -p 8000:8000 todoapp
```

## Testing
To run the tests, use the following command:
```bash
pytest tests
```

## Contributing
Contributions are welcome. Please submit a pull request with your changes.

## License
TodoApp is licensed under the MIT License. See LICENSE for details.

## Authors
- [Your Name]

## Acknowledgments
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Version
1.0.0

## Changelog
- Initial release

## Contact
For questions or issues, please contact [Your Email].