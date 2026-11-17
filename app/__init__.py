import os
from flask import Flask
from config import config
from app.extensions import db, migrate

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

    # Register Blueprints
    from app.main import main_bp
    from app.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
