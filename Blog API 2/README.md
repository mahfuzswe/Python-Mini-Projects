# Blog API

A simple blog platform API built with FastAPI.

## Features

- Create, read, update, and delete blog posts.
- Uses MySQL as the database backend.
- Pydantic for data validation.
- Dependency injection for managing database connections.

## Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://your-repo-url.git
   ```

2. **Change into the project directory:**
   ```bash
   cd "\blog api"
   ```

3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv env
   env\Scripts\activate   # On Windows
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Create and edit a `.env` file if needed to configure your database connection and other settings.

## Running the Application

Start the FastAPI server using uvicorn:
```bash
uvicorn main:app --reload
```

Access the automatically generated API documentation at:
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

## License

Provide the appropriate license details for your project here.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)