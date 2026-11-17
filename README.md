# Blogging Platform with Flask (Week 3: Blog Post CRUD Functionality)

A modular, production-ready web application built with Flask for the **Blogging Platform with Flask** internship.

Building upon Week 1 (Application Factory, Blueprints, SQLAlchemy, Flask-Migrate) and Week 2 (User Authentication & Flask-Login), **Week 3** delivers complete **Blog Post CRUD Functionality**, **Category and Tag relational models**, **Flask-WTF form validation**, and an integrated **Rich Text Editor**.

---

## 🌟 Key Features

### Week 3: Blog Post CRUD, Categories, Tags & Rich Text
- **Complete CRUD Operations**:
  - **Create**: Compose and publish posts via `/posts/new` (guarded by `@login_required`).
  - **Read**: Browse all posts at `/posts/`, filter by category at `/posts/category/<slug>`, filter by tag at `/posts/tag/<slug>`, or view detailed articles at `/posts/<id>`.
  - **Update**: Edit existing articles at `/posts/<id>/edit` (author-only authorization).
  - **Delete**: Remove articles safely via CSRF-protected form at `/posts/<id>/delete` (author-only authorization).
- **Relational Models & Taxonomy**:
  - `Category`: One-to-Many relationship with `Post`.
  - `Tag` & `post_tags`: Many-to-Many association table allowing multi-tagging per article.
- **Flask-WTF Forms**:
  - Form validation with CSRF protection (`PostForm`, `CategoryForm`, `DeleteForm`).
  - Dynamic category dropdown selector and comma-separated tag parsing.
- **Rich Text Editor (Quill.js)**:
  - Integrated rich text editor supporting headings, bold/italic, lists, blockquotes, and code blocks.
  - Automatic synchronization with the underlying Flask-WTF textarea on submission.

### Week 2: User Authentication & Sessions
- **Flask-Login** session management with `UserMixin` and `@login_manager.user_loader`.
- User registration and login with salted one-way password hashing via Werkzeug security.
- Route protection with `@login_required` and dynamic session-aware UI.

### Week 1: Core Architecture
- **Application Factory Pattern** (`create_app()`) supporting multiple environments (`config.py`).
- **Modular Blueprints**: `main_bp`, `auth_bp`, `posts_bp`, and `api_bp`.
- **Database Migrations**: Alembic version control tracked through Flask-Migrate (`migrations/`).

---

## 📁 Project Directory Structure

```text
Blogging-Platform-with-Flask/
├── app/
│   ├── __init__.py          # create_app() factory, registers all blueprints
│   ├── extensions.py        # SQLAlchemy, Flask-Migrate, Flask-Login
│   ├── models.py            # User, Post, Category, Tag models & post_tags association
│   ├── forms.py             # Flask-WTF forms (PostForm, CategoryForm, DeleteForm)
│   ├── posts/               # Posts & Categories Blueprint (CRUD)
│   │   ├── __init__.py
│   │   └── routes.py        # List, create, read, edit, delete, category & tag views
│   ├── auth/                # Auth Blueprint (Flask-Login)
│   │   ├── __init__.py
│   │   └── routes.py        # Register, login, logout, profile
│   ├── main/                # Main Blueprint (presentation & health)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── api/                 # RESTful JSON API Blueprint
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Navbar, flash messages, footer
│   │   ├── index.html       # Home dashboard
│   │   ├── about.html       # System architecture documentation
│   │   ├── auth/            # login.html, register.html, profile.html
│   │   └── posts/           # create.html (Quill.js), detail.html, list.html, category.html, tag.html, categories.html
│   └── static/              # CSS & JS assets
├── migrations/              # Alembic database migration scripts
├── tests/                   # Automated unit test suite (20 tests)
│   ├── __init__.py
│   ├── test_basics.py       # Factory & baseline tests
│   ├── test_auth.py         # Registration & login tests
│   └── test_posts.py        # Post CRUD, authorization & taxonomy tests
├── instance/                # SQLite database storage (gitignored)
├── config.py                # Environment configuration classes
├── run.py                   # Application entrypoint & CLI shell context
├── requirements.txt         # Pinned project dependencies
├── .env.example             # Template for environment variables
├── .gitignore               # Git ignore rules
└── README.md                # Comprehensive documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Clone & Setup
```bash
git clone https://github.com/vedant1399/Blogging-Platform-with-Flask.git
cd Blogging-Platform-with-Flask

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env    # On Windows
cp .env.example .env      # On macOS/Linux

# Run database migrations
flask db upgrade

# Start development server
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Running Automated Tests

Run the full automated test suite:
```bash
python -m unittest discover tests
```
**Status: 20/20 unit tests passing.**

---

## 📡 Routes & Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | Home page dashboard |
| `GET` | `/posts/` | Public | Explore all blog articles |
| `GET, POST` | `/posts/new` | Logged In | Create post (Flask-WTF + Quill.js editor) |
| `GET` | `/posts/<id>` | Public | View article detail with category & tags |
| `GET, POST` | `/posts/<id>/edit` | Author Only | Edit article (pre-populated form) |
| `POST` | `/posts/<id>/delete` | Author Only | Delete article (CSRF protected) |
| `GET` | `/posts/category/<slug>` | Public | Filter posts by category |
| `GET` | `/posts/tag/<slug>` | Public | Filter posts by tag |
| `GET, POST` | `/posts/categories` | Logged In | Manage and create categories |
| `GET, POST` | `/auth/register` | Public | User registration |
| `GET, POST` | `/auth/login` | Public | User login & session management |
| `GET` | `/auth/logout` | Logged In | Terminate user session |

---

## 📚 References
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
