# Blogging Platform with Flask (Week 7: Deployment Preparation & Testing)

A modular, production-ready web application built with Flask for the **Blogging Platform with Flask** internship.

Building upon Weeks 1 through 6, **Week 7** completes the platform with **Deployment Preparation and Comprehensive Testing**: a robust automated unit test suite (45 unit tests across 7 test modules), production WSGI callable (`wsgi.py`), tuned Gunicorn configuration (`gunicorn.conf.py`), multi-stage Docker containerization (`Dockerfile`, `.dockerignore`), multi-container orchestration (`docker-compose.yml`), custom HTTP error pages (404, 403, 500), and automated GitHub Actions Continuous Integration (CI).

---

## 🌟 Key Features

### Week 7: Deployment Preparation & Automated Testing
- **Comprehensive Unit Testing Suite**:
  - 45 automated unit tests spanning 7 test modules (`test_basics.py`, `test_auth.py`, `test_posts.py`, `test_frontend_pagination.py`, `test_comments.py`, `test_search_filter.py`, `test_deployment.py`).
  - Tests covering application factory, configuration switching, authentication, CRUD, pagination, comments cascade deletion, full-text search, category/tag filtering, error pages, and WSGI compatibility.
- **Production WSGI Callable (`wsgi.py`)**:
  - Standards-compliant WSGI entrypoint exposing `app` for production servers like Gunicorn and uWSGI.
- **Tuned Gunicorn Configuration (`gunicorn.conf.py`)**:
  - Multi-process worker management (`2 * CPU + 1`), sync workers, request backlog, worker timeout (120s), and stdout/stderr logging integration.
- **Docker Containerization (`Dockerfile` & `.dockerignore`)**:
  - Lightweight `python:3.12-slim` base image.
  - Principle of least privilege: runs under an unprivileged user `appuser` (UID 1000).
  - Built-in `HEALTHCHECK` probing the `/health` endpoint.
- **Docker Compose (`docker-compose.yml`)**:
  - One-command startup (`docker compose up --build`).
  - Persistent volume binding for `./instance` to preserve database and uploads across container recycles.
- **Custom HTTP Error Handlers**:
  - User-friendly and brand-consistent Jinja2 error templates for **404 Not Found**, **403 Forbidden**, and **500 Internal Server Error** in `app/templates/errors/`.
- **Continuous Integration (CI)**:
  - GitHub Actions workflow (`.github/workflows/tests.yml`) testing on Python 3.11 and 3.12 across every push and pull request.

### Week 6: Search & Filtering Engine
- **Search Across Title & Content**: Full case-insensitive search using SQLAlchemy `or_()` and `ilike()`.
- **Taxonomy Filtering**: Filter by Category or Tag slug.
- **Dynamic Sorting**: Newest, Oldest, and Most Commented/Popular.

### Week 5: Commenting System
- Relational `Comment` model linked to `User` and `Post` with cascade deletion.
- Flask-WTF `CommentForm` with CSRF protection and input validation.
- Dual-authorization moderation (comment author and article owner can delete comments).

### Week 4: Frontend, Navigation & Pagination
- Reusable Jinja2 macros (`render_pagination`, `render_post_card`).
- Full database-backed pagination across Home, Posts, Categories, Tags, and Profiles.
- Individual post view with breadcrumbs and sequential Previous/Next article navigation.
- Public author profile pages (`/users/<username>`).

### Week 3: Blog Post CRUD & Taxonomy
- Complete CRUD operations guarded by author-level authorization.
- `Category` (One-to-Many) and `Tag` (Many-to-Many) relational models.
- Flask-WTF forms and Quill.js Rich Text Editor integration.

### Week 2: User Authentication & Sessions
- User registration, login, logout, and session management using **Flask-Login**.
- Secure salted one-way password hashing using Werkzeug security.
- Route protection with `@login_required` and dynamic session-aware UI.

### Week 1: Core Architecture & Migrations
- Application Factory pattern (`create_app()`) supporting multi-environment configurations.
- Modular Blueprints (`main_bp`, `auth_bp`, `posts_bp`, `api_bp`).
- Database migrations managed via Alembic and Flask-Migrate (`migrations/`).

---

## 📁 Project Directory Structure

```text
Blogging-Platform-with-Flask/
├── .github/
│   └── workflows/
│       └── tests.yml        # GitHub Actions CI workflow (Python 3.11 & 3.12)
├── app/
│   ├── __init__.py          # create_app() factory, error handlers, template filters
│   ├── extensions.py        # SQLAlchemy, Flask-Migrate, Flask-Login
│   ├── models.py            # User, Post, Category, Tag, Comment models & associations
│   ├── forms.py             # Flask-WTF forms (PostForm, CategoryForm, CommentForm, DeleteForm)
│   ├── posts/               # Posts, Categories, Comments, Search & Filter Blueprint
│   ├── auth/                # Auth Blueprint (Flask-Login)
│   ├── main/                # Main Blueprint (home, author profiles, about, health)
│   ├── api/                 # RESTful JSON API Blueprint
│   ├── templates/           # Jinja2 templates
│   │   ├── _macros.html     # Reusable pagination & post card macros
│   │   ├── base.html        # Responsive navbar with global search, flash banners, footer
│   │   ├── index.html       # Home dashboard with paginated feed
│   │   ├── about.html       # Architecture & deployment documentation
│   │   ├── errors/          # Custom HTTP error pages (403.html, 404.html, 500.html)
│   │   ├── users/
│   │   │   └── profile.html # Public author profile & paginated publications
│   │   ├── auth/            # login.html, register.html, profile.html
│   │   └── posts/           # list.html, detail.html, create.html, categories.html
│   └── static/              # CSS assets
├── migrations/              # Alembic database migration scripts
├── tests/                   # Automated unit test suite (45 unit tests)
│   ├── __init__.py
│   ├── test_basics.py       # Factory & baseline tests
│   ├── test_auth.py         # Registration & login tests
│   ├── test_posts.py        # Post CRUD & authorization tests
│   ├── test_frontend_pagination.py # Pagination, navigation, filters & profile tests
│   ├── test_comments.py     # Comment creation, cascade deletion & moderation tests
│   ├── test_search_filter.py# Search by title/content, category/tag filter & sort tests
│   └── test_deployment.py   # WSGI, Gunicorn configs, error handlers & healthcheck tests
├── instance/                # SQLite database storage (gitignored)
├── Dockerfile               # Production Docker container definition
├── docker-compose.yml       # Multi-container local orchestration
├── .dockerignore            # Docker build ignore rules
├── gunicorn.conf.py         # Production Gunicorn configuration
├── wsgi.py                  # Production WSGI application entrypoint
├── config.py                # Environment configuration classes
├── run.py                   # Development application entrypoint
├── requirements.txt         # Pinned project dependencies
├── .env.example             # Template for environment variables
├── .gitignore               # Git ignore rules
└── README.md                # Comprehensive documentation
```

---

## 🚀 Deployment & Quick Start Guide

### 1. Local Development
```bash
git clone https://github.com/vedant1399/Blogging-Platform-with-Flask.git
cd Blogging-Platform-with-Flask

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations & start server
flask db upgrade
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

### 2. Production with Gunicorn
Run the production WSGI server using the tuned configuration:
```bash
gunicorn -c gunicorn.conf.py wsgi:app
```

### 3. Docker Deployment
Build and run the containerized app:
```bash
# Using Docker directly
docker build -t blogging-platform-flask .
docker run -d -p 5000:5000 -v $(pwd)/instance:/app/instance --name flask-app blogging-platform-flask

# Or using Docker Compose (Recommended)
docker compose up --build -d
```
Access the application at **`http://localhost:5000`**. Check status via `http://localhost:5000/health`.

---

## 🧪 Running Automated Tests

Run the full automated test suite:
```bash
python -m unittest discover tests
```
**Status: 45/45 unit tests passing.**

---

## 📡 Routes & Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | Home page with paginated feed & category navigation |
| `GET` | `/health` | Public | Container & orchestrator health check endpoint |
| `GET` | `/posts/` | Public | Explore articles with search (`?q=`), category (`?category=`), tag (`?tag=`), and sort (`?sort=`) |
| `GET` | `/posts/search` | Public | Search redirect endpoint |
| `GET` | `/posts/<id>` | Public | Full post view with comments & prev/next links |
| `POST` | `/posts/<id>/comments` | Logged In | Post a comment on an article |
| `POST` | `/posts/comments/<id>/delete` | Author/Owner | Delete a comment |
| `GET` | `/users/<username>` | Public | Public author profile with paginated articles |
| `GET` | `/posts/category/<slug>` | Public | Category-filtered paginated articles |
| `GET` | `/posts/tag/<slug>` | Public | Tag-filtered paginated articles |
| `GET, POST` | `/posts/new` | Logged In | Create article with Quill.js rich text editor |
| `GET, POST` | `/posts/<id>/edit` | Author Only | Edit article (author only) |
| `POST` | `/posts/<id>/delete` | Author Only | Delete article (author only) |
| `GET, POST` | `/auth/login` | Public | User login & session management |
| `GET, POST` | `/auth/register` | Public | Author registration |

---

## 📚 References
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [Flask Deploying Documentation](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [SQLAlchemy ORM Querying Guide](https://www.sqlalchemy.org/library.html#orm-querying)
- [Flask SQLite3 Patterns](https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
