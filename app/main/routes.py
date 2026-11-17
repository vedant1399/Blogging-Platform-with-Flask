from flask import render_template, jsonify
from app.main import main_bp
from app.models import User, Post

@main_bp.route('/')
def index():
    """Home landing page with list of posts and users."""
    users = User.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', users=users, posts=posts)

@main_bp.route('/about')
def about():
    """About project page."""
    return render_template('about.html')

@main_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'project': 'Blogging Platform with Flask',
        'message': 'Flask application running with Blueprints, SQLAlchemy, and Flask-Migrate'
    }), 200
