from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main import main_bp
from app.extensions import db
from app.models import User, Post

@main_bp.route('/')
def index():
    """Home landing page with list of posts and authors."""
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
        'week': 'Week 2: User Authentication with Flask-Login',
        'auth_enabled': True
    }), 200

@main_bp.route('/create-post', methods=['POST'])
@login_required
def create_post_form():
    """Create post protected route using Flask-Login session."""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        flash('Title and content are required.', 'danger')
        return redirect(url_for('main.index'))

    post = Post(title=title, content=content, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    flash(f'Post "{title}" published successfully!', 'success')
    return redirect(url_for('main.index'))
