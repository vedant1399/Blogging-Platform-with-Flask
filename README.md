# Blogging Platform with Flask (Week 5: Commenting System)

A modular, production-ready web application built with Flask for the **Blogging Platform with Flask** internship.

Building upon Week 1 (Core Architecture & Migrations), Week 2 (Authentication & Sessions), Week 3 (CRUD & Taxonomy), and Week 4 (Frontend, Navigation & Pagination), **Week 5** delivers a complete **Interactive Commenting System** with relational models, Flask-WTF validation, and author/moderator deletion controls.

---

## 🌟 Key Features

### Week 5: Commenting System
- **Relational Comment Model**:
  - Links to `User` (author) and `Post` (article) via foreign keys.
  - Cascade deletion enabled: deleting an article automatically removes all of its associated comments.
- **Flask-WTF CommentForm**:
  - Input length and content validation (`DataRequired`, `Length(2, 1000)`).
  - Built-in CSRF token protection.
- **Granular Permissions & Moderation**:
  - Submitting comments requires an authenticated session (`@login_required`).
  - Comment deletion permitted for either the **comment author** OR the **post owner** (enabling article moderation).
- **Interactive UI**:
  - Live comment count indicators across article headers, cards, and author profiles.
  - Direct comment posting and instant feedback via flash messages.

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
├── app/
│   ├── __init__.py          # create_app() factory, custom filters (reading_time, format_datetime)
│   ├── extensions.py        # SQLAlchemy, Flask-Migrate, Flask-Login
│   ├── models.py            # User, Post, Category, Tag, Comment models & associations
│   ├── forms.py             # Flask-WTF forms (PostForm, CategoryForm, CommentForm, DeleteForm)
│   ├── posts/               # Posts, Categories & Comments Blueprint
│   ├── auth/                # Auth Blueprint (Flask-Login)
│   ├── main/                # Main Blueprint (home, author profiles, about, health)
│   ├── api/                 # RESTful JSON API Blueprint
│   ├── templates/           # Jinja2 templates
│   │   ├── _macros.html     # Reusable pagination & post card macros
│   │   ├── base.html        # Responsive navbar, flash banners, footer
│   │   ├── index.html       # Home dashboard with paginated feed
│   │   ├── about.html       # Architecture documentation
│   │   ├── users/
│   │   │   └── profile.html # Public author profile & paginated publications
│   │   ├── auth/            # login.html, register.html, profile.html
│   │   └── posts/           # create.html (Quill), detail.html (comments & prev/next), list.html, category.html, tag.html, categories.html
│   └── static/              # CSS assets
├── migrations/              # Alembic database migration scripts
├── tests/                   # Automated unit test suite (32 tests)
│   ├── __init__.py
│   ├── test_basics.py       # Factory & baseline tests
│   ├── test_auth.py         # Registration & login tests
│   ├── test_posts.py        # Post CRUD & authorization tests
│   ├── test_frontend_pagination.py # Pagination, navigation, filters & profile tests
│   └── test_comments.py     # Comment creation, cascade deletion & moderation tests
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
**Status: 32/32 unit tests passing.**

---

## 📡 Routes & Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | Home page with paginated feed & category navigation |
| `GET` | `/posts/` | Public | Explore all articles with paginated browsing |
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
- [Flask SQLite3 Patterns](https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
