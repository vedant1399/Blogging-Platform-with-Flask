from flask import render_template, jsonify, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.main import main_bp
from app.extensions import db
from app.models import User, Post, Category

@main_bp.route('/')
def index():
    """Home landing page with paginated articles and category navigation."""
    page = request.args.get('page', 1, type=int)
    per_page = 4
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    categories = Category.query.order_by(Category.name).all()
    users = User.query.all()
    return render_template('index.html', pagination=pagination, posts=posts, categories=categories, users=users)

@main_bp.route('/users/<username>')
def user_profile(username):
    """Public author profile page with paginated authored articles."""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = user.posts.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template('users/profile.html', user=user, pagination=pagination, posts=posts)

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
        'week': 'Week 4: Frontend: Displaying Posts and Navigation (Pagination & Jinja2 Templates)',
        'auth_enabled': True
    }), 200

@main_bp.route('/create-post', methods=['POST'])
@login_required
def create_post_form():
    """Create post quick action via form."""
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
