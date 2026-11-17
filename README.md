# Blogging Platform with Flask (Week 2: User Authentication)

A modular, production-ready Flask application serving as the foundation for the **Blogging Platform with Flask** internship project. 

Building upon Week 1's architecture (Application Factory, Blueprints, SQLAlchemy, Flask-Migrate), **Week 2** adds full **User Authentication & Session Management** using **Flask-Login** and **Werkzeug Security**.

---

## 🌟 Key Features

### Week 2: User Authentication & Sessions
- **User Registration**: `/auth/register` with validation (duplicate checks, minimum password length, password confirmation).
- **Secure Password Hashing**: Cryptographic one-way hashing with salt using Werkzeug (`generate_password_hash` & `check_password_hash`).
- **Session Management with Flask-Login**:
  - `UserMixin` model integration.
  - `@login_manager.user_loader` session loader.
  - Remember-me cookie support.
  - Safe post-login redirection using `next` query parameter.
- **Access Control & Protected Routes**: Guarded with `@login_required` (e.g. creating posts, accessing `/auth/profile`, logging out).
- **Responsive Dynamic UI**: Navigation bar and actions adapt dynamically based on `current_user.is_authenticated`.

### Week 1: Core Architecture
- **Application Factory Pattern**: Implemented in `app/__init__.py` using `create_app()` with multi-environment support (`development`, `testing`, `production`).
- **Modular Blueprints**:
  - `auth_bp`: User authentication & session routes.
  - `main_bp`: Frontend web routes (`/`, `/about`, `/health`, `/create-post`).
  - `api_bp`: RESTful JSON API endpoints (`/api/users`, `/api/posts`).
- **Database Architecture (SQLAlchemy & Flask-Migrate)**:
  - Models: `User` and `Post` with one-to-many relationship, foreign keys, timestamps, indexes, and JSON serialization.
  - Alembic migrations in `migrations/` directory to manage and track schema evolution safely.
- **Automated Testing Suite**: Comprehensive unit tests covering authentication, registration, login/logout, factory instantiation, blueprints, models, and API endpoints (**13/13 tests passing**).

---

## 📁 Project Directory Structure

```text
Blogging-Platform-with-Flask/
├── app/
│   ├── __init__.py          # create_app() factory, registers main, auth, and api blueprints
│   ├── extensions.py        # SQLAlchemy, Flask-Migrate, and Flask-Login instances
│   ├── models.py            # User (UserMixin) and Post SQLAlchemy models with hashing
│   ├── auth/                # Auth Blueprint (Flask-Login)
│   │   ├── __init__.py
│   │   └── routes.py        # /auth/register, /auth/login, /auth/logout, /auth/profile
│   ├── main/                # Main frontend Blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Home (/), About (/about), Health (/health), /create-post
│   ├── api/                 # RESTful API Blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Users and Posts JSON endpoints
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base layout with responsive navbar and flash message banners
│   │   ├── index.html       # Blog dashboard with dynamic auth state & post creation
│   │   ├── about.html       # Architecture overview page
│   │   └── auth/
│   │       ├── login.html   # Login form with remember me
│   │       ├── register.html# Registration form
│   │       └── profile.html # User profile showing authored posts
│   └── static/              # Static assets (CSS/JS)
├── migrations/              # Flask-Migrate (Alembic) version control scripts
├── tests/                   # Automated unit test suite
│   ├── __init__.py
│   ├── test_basics.py       # Factory, blueprint, model, and API tests
│   └── test_auth.py         # Authentication, registration, login, logout & session tests
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

### 7. Run the Application
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

Run the full test suite to verify application & authentication integrity:
```bash
python -m unittest discover tests
```

---

## 📡 Key Routes

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | Home page blog dashboard |
| `GET, POST` | `/auth/register` | Public | User registration with password hashing |
| `GET, POST` | `/auth/login` | Public | User login with session management |
| `GET` | `/auth/logout` | Logged In | User logout & session termination |
| `GET` | `/auth/profile` | Logged In | Authenticated user profile |
| `POST` | `/create-post` | Logged In | Publish a new blog post |
| `GET` | `/api/posts` | Public | Retrieve list of all blog posts (JSON) |
| `GET` | `/api/users` | Public | Retrieve list of all users/authors (JSON) |

---

## 📚 References
- [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
- [Flask Official Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
