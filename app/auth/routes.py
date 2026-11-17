from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlsplit
from app.auth import auth_bp
from app.extensions import db
from app.models import User, Post

def is_safe_url(target):
    """Ensure redirect URL is on the same host."""
    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(target)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc or not test_url.netloc


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html', username=username, email=email)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html', username=username, email=email)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', username=username, email=email)

        if User.query.filter_by(username=username).first():
            flash('Username is already taken. Please choose another.', 'danger')
            return render_template('auth/register.html', username=username, email=email)

        if User.query.filter_by(email=email).first():
            flash('Email is already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        # Create user and hash password
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not identifier or not password:
            flash('Please enter your username/email and password.', 'danger')
            return render_template('auth/login.html', identifier=identifier)

        # Allow login via username or email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(password):
            flash('Invalid username/email or password.', 'danger')
            return render_template('auth/login.html', identifier=identifier)

        # Log user in and manage session
        login_user(user, remember=remember)
        flash(f'Welcome back, {user.username}!', 'success')

        next_page = request.args.get('next')
        if not next_page or not is_safe_url(next_page):
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """Protected user dashboard route with paginated posts."""
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template('auth/profile.html', user=current_user, pagination=pagination, posts=posts)
