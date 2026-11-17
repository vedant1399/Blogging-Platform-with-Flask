import os
import re
from flask import Flask, render_template
from config import config
from app.extensions import db, migrate, login_manager

def create_app(config_name=None):
    """Application Factory pattern implementation."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance'), exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Custom Jinja2 Filters for Frontend Templates
    @app.template_filter('reading_time')
    def reading_time_filter(html_text):
        """Calculate estimated reading time from HTML text."""
        words = len(re.findall(r'\w+', re.sub(r'<[^>]+>', '', html_text or '')))
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"

    @app.template_filter('format_datetime')
    def format_datetime_filter(dt, format='%B %d, %Y'):
        """Format datetime object into human-readable string."""
        if dt is None:
            return ''
        return dt.strftime(format)

    # Custom Production Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Register Blueprints
    from app.main import main_bp
    from app.api import api_bp
    from app.auth import auth_bp
    from app.posts import posts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    return app
