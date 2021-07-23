import os
import logging

from flask import Flask
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_jwt import JWT
#

db = SQLAlchemy()
migrate = Migrate()
flask_mail = Mail()
login = LoginManager()
login.login_view = 'loginauth.login'
login.login_message = 'Please login to access this page'

bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    # help(mail)
    flask_mail.init_app(app)
    # print(inspect.getsource(mail))
    bootstrap.init_app(app)

    from app.jwt import authenticate, identity

    JWT(app, authenticate, identity)
    from app.errors import errors_blueprint
    app.register_blueprint(errors_blueprint)

    from app.auth import ab
    app.register_blueprint(ab)

    from app.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from app.post import post_blueprint
    app.register_blueprint(post_blueprint)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure=()

            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@'+app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Microblog failuer',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Microblog startup')
    return app
