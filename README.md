# Notes API

A RESTful API for sharing and managing personal notes, built with FastAPI and PostgreSQL.
Users can register, authenticate, and perform full CRUD operations on their own notes.

## Tech Stack
FastAPI · PostgreSQL · SQLAlchemy · Pydantic · JWT · bcrypt · pytest

## Features
- JWT authentication
- Password hashing with bcrypt
- Async database operations
- Data validation with custom validators
- Unit tests with pytest

## Installation

1. Clone and install
```bash
   git clone https://github.com/tamerlan-islamzade/Note-API.git
   cd Note-API
   pip install -r requirements.txt
```

2. Create `.env`
```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Run
```bash
   uvicorn main:app --reload
```

Docs available at `http://localhost:8000/docs`

## Tests
```bash
pytest -v
```# Note-API-private
