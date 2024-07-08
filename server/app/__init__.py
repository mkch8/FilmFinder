from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # Import and register blueprints
    with app.app_context():
        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
