from flask import Flask, jsonify # pyright: ignore[reportMissingImports]
import os
from .schema.models import db
from flask_jwt_extended import JWTManager # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from flask_migrate import Migrate # pyright: ignore[reportMissingImports]
from .constants.http_status_codes import HTTP_429_TOO_MANY_REQUESTS, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

limiter = Limiter(
    get_remote_address,
    default_limits=["100 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="moving-window",
)  


# initiate app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
            JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
            API_KEY=os.getenv('API_KEY'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)
    
    # initialise the database here
    db.app=app
    db.init_app(app)
    
    # initialise jwt here
    JWTManager(app)
    # initialise migrations
    Migrate(app, db)
    # initialise the limiter here
    limiter.init_app(app)


    # import more blueprints
    from .auth.user_auth import auth
    from .routes.generate_stories import story_bp
    from .routes.character_chat import chat_bp
    
    # configure blueprints here
    app.register_blueprint(auth)
    app.register_blueprint(story_bp)
    app.register_blueprint(chat_bp)
    
    # exception handling | catch runtime errors here
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_file_not_found(error):
        return jsonify({'error': f"{HTTP_404_NOT_FOUND} File not found!"}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_internalServer_error(error):
        return jsonify({'error': "Something went wrong!"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    @app.errorhandler(HTTP_503_SERVICE_UNAVAILABLE)
    def handle_connection_error(error):
        return jsonify({'error': "Service is currently unavailable. Our team is working on it!"}), HTTP_503_SERVICE_UNAVAILABLE

    @app.errorhandler(HTTP_429_TOO_MANY_REQUESTS)
    def handle_too_many_requests(error):
        return jsonify({'error': "You have reached your limit for the day. Please try again after 24 hours."}), HTTP_429_TOO_MANY_REQUESTS


    return app