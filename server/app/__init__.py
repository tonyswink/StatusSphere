from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions without binding them to a specific app
db = SQLAlchemy()

def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind extensions to the app
    db.init_app(app)

    # Register blueprints
    from app.routes.status import status_blueprint
    app.register_blueprint(status_blueprint, url_prefix='/api/statuses')

    from app.routes.icons import icons_blueprint
    app.register_blueprint(icons_blueprint, url_prefix='/api/icons')

    from app.routes.colours import colours_blueprint
    app.register_blueprint(colours_blueprint, url_prefix='/api/colours')

    # It's a good practice to create the database tables from here
    with app.app_context():
        db.create_all()

    return app
