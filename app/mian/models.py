from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app import Model, db
from app.book.spider import YuShuBook


class Gift(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User', backref='gifts')
    user_id = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    is_launched = Column(Boolean, default=False)

    @classmethod
    def recent(cls):
        count = current_app.config['RECENT_BOOK_COUNT']
        recent_gifts = (cls.query
                        .filter_by(is_launched=False)
                        .group_by(cls.isbn)
                        .order_by(desc(cls.create_time))
                        .limit(count)
                        .all())
        return recent_gifts

    @property
    def book(self):
        ys_book = YuShuBook()
        ys_book.search_by_isbn(self.isbn)
        return ys_book.first

    @classmethod
    def get_user_gifts(cls, user_id):
        gifts = (cls.query
                 .filter_by(user_id=user_id, is_launched=False)
                 .order_by(desc(cls.create_time))
                 .all())
        return gifts

    @classmethod
    def get_wishes_counts(cls, iterable):
        count_list = (db.session
                      .query(func.count(Wish.id), Wish.isbn).
                      filter(Wish.is_launched == False,
                             Wish.isbn.in_(iterable),
                             Wish.is_void == False)
                      .group_by(Wish.isbn))
        return [{'count': c[0], 'isbn': c[0]} for c in count_list]

    def is_yourself_gift(self, user_id):
        return self.user_id == user_id


class Wish(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User', backref='wishes')
    user_id = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    is_launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, user_id):
        wishes = (cls.query
                  .filter_by(user_id=user_id, is_launched=False)
                  .order_by(desc(cls.create_time))
                  .all())
        return wishes

    @classmethod
    def get_gifts_counts(cls, iterable):
        count_list = (db.session
                      .query(func.count(Wish.id), Wish.isbn).
                      filter(Gift.is_launched == False,
                             Gift.isbn.in_(iterable),
                             Gift.is_void == False)
                      .group_by(Wish.isbn))
        return [{'count': c[0], 'isbn': c[0]} for c in count_list]

    @property
    def book(self):
        ys_book = YuShuBook()
        ys_book.search_by_isbn(self.isbn)
        return ys_book.first

