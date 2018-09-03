from flask import request, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.mian.models import Gift, Wish
from . import book
from .spider import YuShuBook
from .forms import SearchForm
from .viewmodels import Books, Book, TradeInfo


@book.route('/book/search')
def search():
    """
    param:
            q: 关键字 isbn
            page
    """
    form = SearchForm(request.args)
    books = Books()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        ys_book = YuShuBook()

        if isbn_or_key == 'isbn':
            ys_book.search_by_isbn(q)

        else:
            ys_book.search_by_keyword(q, page)

        books.fill(ys_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入')
    return render_template('book/search_result.html', books=books)


@book.route('/book/<isbn>')
def detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    ys_book = YuShuBook()
    ys_book.search_by_isbn(isbn)
    book_ = Book(ys_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(user_id=current_user.id,
                                isbn=isbn,
                                is_launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(user_id=current_user.id,
                                isbn=isbn,
                                is_launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, is_launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, is_launched=False).all()

    gifts = TradeInfo(trade_gifts)
    wishes = TradeInfo(trade_wishes)

    return render_template('book/detail.html',
                           book=book_,
                           wishes=wishes,
                           gifts=gifts,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)
