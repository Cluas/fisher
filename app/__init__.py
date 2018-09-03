from contextlib import contextmanager
from datetime import datetime

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from flask_login import LoginManager

from sqlalchemy import Column, Boolean, Integer

from .libs.helper import timestamp
from config import config


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):

    def filter_by(self, **kwargs):
        if 'is_void' not in kwargs.keys():
            kwargs['is_void'] = False
        return super().filter_by(**kwargs)


login_manager = LoginManager()
db = SQLAlchemy(query_class=Query)
mail = Mail()


class Model(db.Model):
    __abstract__ = True
    create_time = Column(Integer, default=timestamp)
    is_void = Column(Boolean, default=False)

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)

    def delete(self):
        self.is_void = True


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    register_blueprints(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登陆或注册'
    return app


def register_blueprints(app):
    from .mian import main
    from .book import book
    from .auth import auth
    from .drift import drift
    app.register_blueprint(main)
    app.register_blueprint(book)
    app.register_blueprint(auth)
    app.register_blueprint(drift)
