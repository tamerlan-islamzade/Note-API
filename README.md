## Notes API
## Features
- JWT authentication
- Password hashing with bcrypt
- Async database operations with SQLAlchemy
- Data validation with Pydantic

## Tech Stack
- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — async ORM
- **Pydantic** — schema validation
- **JWT** — authentication

## Getting Started

### Requirements
- Python 3.11+
- PostgreSQL

### Installation
1. Clone the repository
```bash
   git clone https://github.com/yourusername/notes-api.git
   cd notes-api
```

2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. Create a `.env` file in the root directory
```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run the application
```bash
   uvicorn main:app --reload
```

5. Visit the docs at `http://localhost:8000/docs`# Note-API
