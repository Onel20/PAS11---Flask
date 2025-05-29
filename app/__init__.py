from flask import Flask
from app.config import Config
from app.controllers.routes import routes_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'your-secret-key'  # change this to a secure secret key

    app.register_blueprint(routes_blueprint)

    return app