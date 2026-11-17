import re
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


def slugify(text):
    """Generate a clean URL slug from string."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text).strip('-')


class User(UserMixin, db.Model):
    """User database model with Flask-Login and password hashing."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to Blog Posts
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password against the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'post_count': self.posts.count()
        }

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return db.session.get(User, int(user_id))


# Many-to-Many Association Table between Posts and Tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Category(db.Model):
    """Blog Category model."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)

    # One-to-Many relationship with Posts
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name, description=None, slug=None):
        self.name = name
        self.description = description
        self.slug = slug or slugify(name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'post_count': self.posts.count()
        }

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    """Blog Tag model."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    slug = db.Column(db.String(40), unique=True, nullable=False, index=True)

    def __init__(self, name, slug=None):
        self.name = name.strip()
        self.slug = slug or slugify(name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'post_count': self.posts.count()
        }

    def __repr__(self):
        return f'<Tag {self.name}>'


class Post(db.Model):
    """Blog Post database model with Category and Tags."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(160), nullable=True, index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Many-to-Many with Tag
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, content, user_id, category_id=None, summary=None, slug=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.category_id = category_id
        self.summary = summary or (content[:150] + '...' if len(content) > 150 else content)
        self.slug = slug or slugify(title)

    def get_tags_string(self):
        """Return comma-separated string of tag names."""
        return ', '.join([t.name for t in self.tags])

    def set_tags_from_string(self, tags_string):
        """Associate tags from comma-separated string, creating new ones if needed."""
        self.tags = []
        if not tags_string:
            return
        if self not in db.session:
            db.session.add(self)
        tag_names = [t.strip() for t in tags_string.split(',') if t.strip()]
        for name in tag_names:
            clean_name = name.lower()
            tag = Tag.query.filter_by(name=clean_name).first()
            if not tag:
                tag = Tag(name=clean_name)
                db.session.add(tag)
            self.tags.append(tag)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'summary': self.summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'author': self.author.username if self.author else None,
            'category': self.category.name if self.category else None,
            'tags': [t.name for t in self.tags]
        }

    def __repr__(self):
        return f'<Post {self.title}>'
