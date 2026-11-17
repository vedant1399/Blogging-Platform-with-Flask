# Blogging Platform with Flask (Week 4: Frontend: Displaying Posts and Navigation)

A modular, production-ready web application built with Flask for the **Blogging Platform with Flask** internship.

Building upon Week 1 (Core Architecture & Migrations), Week 2 (Authentication & Sessions), and Week 3 (CRUD & Taxonomy), **Week 4** enhances the **Frontend Experience** with modular Jinja2 templates, a reusable macro-based **Pagination System**, **Individual Post Views** with breadcrumb navigation and prev/next links, and **Public Author Profile Pages**.

---

## 🌟 Key Features

### Week 4: Frontend, Navigation & Pagination
- **Jinja2 Macros & Template Architecture**:
  - `render_pagination`: Reusable numbered pagination with previous/next controls, disabled boundary states, page summaries, and query preservation.
  - `render_post_card`: Consistent, modular card layout displaying categories, tags, estimated reading time, author, and timestamp.
- **Full Database-Backed Pagination**:
  - Implemented across the Home page (`/`), Posts explore listing (`/posts/`), Category archive (`/posts/category/<slug>`), Tag archive (`/posts/tag/<slug>`), and Author profiles (`/users/<username>`).
- **Individual Post View & Enhanced Navigation**:
  - Multi-level breadcrumbs navigation (`Home > Articles > Category > Post Title`).
  - Formatted rich text content display with author card, tags, and timestamps.
  - Sequential **Previous Article** and **Next Article** navigation links.
- **Author Profile Pages**:
  - Public author profile page (`/users/<username>`) displaying author bio, join date, total article count, and a paginated archive of their published articles.
  - Private user dashboard (`/auth/profile`) with quick management shortcuts.
- **Custom Jinja2 Filters**:
  - `reading_time`: Automatically calculates estimated read time based on word count.
  - `format_datetime`: Formats timestamps into human-readable dates.

### Week 3: Blog Post CRUD & Taxonomy
- Complete CRUD operations guarded by author-level authorization.
- `Category` (One-to-Many) and `Tag` (Many-to-Many via `post_tags` association table) relational models.
- Flask-WTF forms (`PostForm`, `CategoryForm`, `DeleteForm`) with CSRF protection.
- Quill.js Rich Text Editor integration with client-side synchronization.

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
│   ├── models.py            # User, Post, Category, Tag models & post_tags association
│   ├── forms.py             # Flask-WTF forms (PostForm, CategoryForm, DeleteForm)
│   ├── posts/               # Posts & Categories Blueprint
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
│   │   └── posts/           # create.html (Quill), detail.html (breadcrumbs & prev/next), list.html, category.html, tag.html, categories.html
│   └── static/              # CSS assets
├── migrations/              # Alembic database migration scripts
├── tests/                   # Automated unit test suite (24 tests)
│   ├── __init__.py
│   ├── test_basics.py       # Factory & baseline tests
│   ├── test_auth.py         # Registration & login tests
│   ├── test_posts.py        # Post CRUD & authorization tests
│   └── test_frontend_pagination.py # Pagination, navigation, filters & profile tests
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
**Status: 24/24 unit tests passing.**

---

## 📡 Routes & Pages

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home page with paginated feed & category navigation |
| `GET` | `/posts/` | Explore all articles with paginated browsing |
| `GET` | `/posts/<id>` | Full post view with breadcrumbs & prev/next links |
| `GET` | `/users/<username>` | Public author profile with paginated authored articles |
| `GET` | `/posts/category/<slug>` | Category-filtered paginated articles |
| `GET` | `/posts/tag/<slug>` | Tag-filtered paginated articles |
| `GET, POST` | `/posts/new` | Create article with Quill.js rich text editor |
| `GET, POST` | `/posts/<id>/edit` | Edit article (author only) |
| `POST` | `/posts/<id>/delete` | Delete article (author only, CSRF protected) |
| `GET, POST` | `/auth/login` | User login & session management |
| `GET, POST` | `/auth/register` | Author registration |
| `GET` | `/auth/profile` | Private user account dashboard |

---

## 📚 References
- [Jinja2 Templates Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
- [Flask-SQLAlchemy Pagination](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/pagination/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
