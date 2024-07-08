from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from loguru import logger


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    logger.add("app.log", rotation="500 MB")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app