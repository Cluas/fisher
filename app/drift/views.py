from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app import db
from app.book.viewmodels import Book
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.mian.models import Gift, Wish
from . import drift as app
from .forms import DriftForm
from .viewmodels import Drifts
from .models import Drift


@app.route('/<int:drift_id>/redraw')
@login_required
def redraw_drift(drift_id):
    with db.auto_commit():
        drift = Drift.query.filter_by(id=drift_id,
                                      requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
        drift.delete()
    return redirect(url_for('drift.pending'))


@app.route('/<int:drift_id>/reject')
@login_required
def reject_drift(drift_id):
    from app.auth.models import User
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == drift_id,
                                   Gift.user_id == current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('drift.pending'))


@app.route('/<int:drift_id>/mailed')
@login_required
def mailed_drift(drift_id):
    with db.auto_commit():
        drift = Drift.query.filter_by(id=drift_id,
                                      contributor_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        Gift.query.filter_by(id=drift.gift_id).update(
            {Gift.is_launched: True}
        )
        Wish.query.filter_by(isbn=drift.isbn,
                             user_id=drift.requester_id,
                             is_launched=False).update(
            {Wish.is_launched: True}
        )
    return redirect(url_for('drift.pending'))


@app.route('/<int:gift_id>', methods=['GET', 'POST'])
@login_required
def send_drift(gift_id):
    gift = Gift.query.get_or_404(gift_id)
    if gift.is_yourself_gift(current_user.id):
        flash("这本书是你自己的(^-^), 不能向自己索要书籍奥")
        return redirect(url_for('book.detail', isbn=gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, gift)
        send_mail(gift.user.email, '有人想要一本书', 'email/get_gift', wisher=current_user, gift=gift)
        return redirect(url_for('drift.pending'))
    contributor = gift.user.summary
    return render_template('drift/drift.html', contributor=contributor, user_beans=current_user.beans, form=form)


@app.route('/pending')
@login_required
def pending():
    drifts = (Drift
              .query
              .filter(or_(Drift.requester_id == current_user.id,
                          Drift.contributor_id == current_user.id))
              .order_by(desc(Drift.create_time))
              .all())
    drifts = Drifts(drifts, current_user.id).data

    return render_template('drift/pending.html', drifts=drifts)


def save_drift(form, gift):
    with db.auto_commit():
        drift = Drift()
        form.populate_obj(drift)

        drift.gift_id = gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.contributor_nickname = gift.user.nickname
        drift.contributor_id = gift.user.id

        book = Book(gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1
        db.session.add(drift)
