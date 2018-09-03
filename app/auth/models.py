from math import floor

from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from app import Model, login_manager, db
from app.book.spider import YuShuBook
from app.drift.models import Drift
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.mian.models import Gift, Wish


class User(UserMixin, Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    nickname = Column(String(24), nullable=False)
    mobile = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    _is_active = Column('is_active', Boolean, default=False)
    beans = Column(Float, default=0)
    contrib_count = Column(Integer, default=0)
    receive_count = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)

    def is_active(self):
        return self._is_active

    def can_save_to_db(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        ys_book = YuShuBook()
        ys_book.search_by_isbn(isbn)
        if not ys_book.first:
            return False
        gifts = Gift.query.filter_by(user_id=self.id, isbn=isbn, is_launched=False).first()
        wishes = Wish.query.filter_by(user_id=self.id, isbn=isbn, is_launched=False).first()
        if gifts or wishes:
            return False
        return True

    @classmethod
    def reset_password(cls, token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception:
            return False
        user_id = data.get('id')
        with db.auto_commit():
            user = User.query.filter_by(id=user_id).first()
            if user:
                user.password = password
        return True

    def generate_token(self, expire=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expire)
        token = s.dumps({'id': self.id}).decode('utf-8')
        return token

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_contrib_count = Gift.query.filter_by(
            user_id=self.id, is_launched=True
        ).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success
        ).count()
        return floor(success_contrib_count / 2) <= floor(success_receive_count)

    @property
    def summary(self):
        summary = dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            contrib_receive='{}/{}'.format(self.contrib_count, self.receive_count)
        )
        return summary


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
