from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.book.viewmodels import Book
from app.drift.models import Drift
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.mian.viewmodels import Trades
from . import main as app
from .models import Gift, Wish


@app.route('/')
def index():
    recent_gifts = Gift.recent()
    recent = [Book(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=recent)


@app.route('/my/wishes')
@login_required
def my_wishes():
    user_id = current_user.id
    wishes = Wish.get_user_wishes(user_id)
    isbn_gen = (wish.isbn for wish in wishes)
    gift_count_list = Wish.get_gifts_counts(isbn_gen)
    wishes = Trades(wishes, gift_count_list)
    return render_template('my_wish.html', wishes=wishes.trades)


@app.route('/my/gifts')
@login_required
def my_gifts():
    user_id = current_user.id
    gifts = Gift.get_user_gifts(user_id)
    isbn_gen = (gift.isbn for gift in gifts)
    wish_count_list = Gift.get_wishes_counts(isbn_gen)
    gifts = Trades(gifts, wish_count_list)
    return render_template('my_gifts.html', gifts=gifts.trades)


@app.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_db(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.user_id = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在你的心愿清单, 请不要重复添加')
    return redirect(url_for('book.detail', isbn=isbn))


@app.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_db(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.user_id = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK'] or 0
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在你的心愿清单, 请不要重复添加')
    return redirect(url_for('book.detail', isbn=isbn))


@app.route('/wish/<int:wish_id>/satisfy')
@login_required
def satisfy_wish(wish_id):
    wish = Wish.query.get_or_404(wish_id)
    gift = Gift.query.filter_by(user_id=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书, 请点击"加入到赠送清单"添加此书, 添加前, 请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人向送你一本书', 'email/satisfy_wish', wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件, 如果他/她愿意接受你的赠送, 你将收到一个鱼漂')
    return redirect(url_for('book.detail', isbn=wish.isbn))


@app.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wishes(isbn):
    wish = Wish.query.filter_by(isbn=isbn, is_launched=False).first_or_404()

    with db.auto_commit():
        current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
        wish.delete()
    return redirect(url_for('main.my_wishes'))


@app.route('/gift/<gift_id>/redraw')
@login_required
def redraw_from_gifts(gift_id):
    gift = Gift.query.filter_by(id=gift_id, is_launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gift_id, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('main.my_gifts'))
