from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging

# Initialize extensions without binding them to a specific app
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind extensions to the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    register_blueprints(app)

    # It's a good practice to create the database tables from here
    with app.app_context():
        db.create_all()

    return app

def configure_logging(app):
    if not app.debug:
        # Configure logging for production
        app.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

def register_blueprints(app):
    from app.routes.status import status_blueprint
    app.register_blueprint(status_blueprint, url_prefix='/api/statuses')

    from app.routes.icons import icons_blueprint
    app.register_blueprint(icons_blueprint, url_prefix='/api/icons')

    from app.routes.colours import colours_blueprint
    app.register_blueprint(colours_blueprint, url_prefix='/api/colours')