# Blogging Platform with Flask (Week 1: Setup & Basic Structure)

A modular, production-ready Flask application serving as the foundation for the **Blogging Platform with Flask** internship project. This implementation establishes the core application architecture, including the Application Factory pattern, modular Blueprints, relational database models via SQLAlchemy ORM, and schema migration tracking via Flask-Migrate (Alembic).

---

## 🌟 Key Features

- **Application Factory Pattern**: Implemented in `app/__init__.py` using `create_app()` with environment-driven configuration (`development`, `testing`, `production`).
- **Modular Blueprints**:
  - `main_bp`: Handles frontend web routes (`/`, `/about`, `/health`) with responsive Jinja2 HTML templates styled with Tailwind CSS.
  - `api_bp`: Provides RESTful JSON API endpoints (`/api/users`, `/api/posts`) for author and blog post management.
- **Database Architecture (SQLAlchemy & Flask-Migrate)**:
  - Models: `User` and `Post` with one-to-many relationship, foreign keys, timestamps, indexes, and JSON serialization.
  - Alembic database migrations in `migrations/` directory to manage and track schema evolution safely.
- **Automated Testing Suite**: Comprehensive unit tests covering factory instantiation, blueprints, models, and API endpoints using Python's `unittest` (**7/7 tests passing**).
- **Environment & Configuration Management**: Centralized configuration in `config.py` and environment variable support via `python-dotenv`.

---

## 📁 Project Directory Structure

```text
Blogging-Platform-with-Flask/
├── app/
│   ├── __init__.py          # create_app() application factory & blueprint registration
│   ├── extensions.py        # SQLAlchemy & Flask-Migrate instances
│   ├── models.py            # User and Post SQLAlchemy ORM models
│   ├── main/                # Main frontend blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Home (/), About (/about), and Health (/health)
│   ├── api/                 # RESTful API blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Users and Posts JSON endpoints
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base responsive layout
│   │   ├── index.html       # Interactive blog dashboard with live User & Post creation
│   │   └── about.html       # Architecture overview page
│   └── static/              # Static assets
│       ├── css/
│       │   └── style.css
│       └── js/
├── migrations/              # Flask-Migrate (Alembic) migration files
│   ├── versions/            # Migration scripts (schema version control)
│   ├── alembic.ini
│   └── env.py
├── tests/                   # Automated unit test suite
│   ├── __init__.py
│   └── test_basics.py       # Factory, blueprint, model, and API tests
├── instance/                # SQLite database storage (gitignored)
├── config.py                # Environment configuration classes
├── run.py                   # Application entrypoint & CLI shell context
├── requirements.txt         # Pinned project dependencies
├── .env.example             # Template for environment variables
├── .gitignore               # Git ignore rules for Python and databases
└── README.md                # Comprehensive documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/vedant1399/Blogging-Platform-with-Flask.git
cd Blogging-Platform-with-Flask
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

### 6. Apply Database Migrations
Run the Flask database migration command to set up the SQLite database:
```bash
flask db upgrade
```
*(Optional: To create a new migration after editing models)*
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### 7. Run the Application
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

Run the test suite to verify application integrity:
```bash
python -m unittest discover tests
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home page blog dashboard (HTML) |
| `GET` | `/about` | Architecture and task documentation |
| `GET` | `/health` | Health status check (JSON) |
| `GET` | `/api/users` | Retrieve list of all users/authors (JSON) |
| `POST` | `/api/users` | Create a new user (`{"username": "...", "email": "..."}`) |
| `GET` | `/api/users/<id>` | Retrieve a user by ID (JSON) |
| `GET` | `/api/posts` | Retrieve list of all blog posts (JSON) |
| `POST` | `/api/posts` | Create a post (`{"user_id": 1, "title": "...", "content": "..."}`) |
| `GET` | `/api/posts/<id>` | Retrieve a blog post by ID (JSON) |
| `DELETE` | `/api/posts/<id>` | Delete a blog post by ID |

---

## 📚 References
- [Flask Official Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
