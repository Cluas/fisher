from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from .forms import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordForm
from .models import User
from . import auth
from app import db


@auth.route('/login', methods=['GET', "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('main.index')
            return redirect(next_url)
        else:
            flash('账号不存在或密码错误')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/forget/password')
def forget_password():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).first_or_404()
            from app.libs.email import send_mail
            send_mail(email, "重置您的密码",
                      'email/reset_password',
                      user=user,
                      token=user.generate_token())
    return render_template('auth/forget_password.html', form=form)


@auth.route('/user/center')
@login_required
def personal_center():
    user = current_user
    return render_template('auth/personal.html', user=user)


@auth.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            current_user.password = form.new_password1.data
        flash('密码已更新成功')
        return redirect(url_for('web.personal'))
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password1.data
        success = User.reset_password(token, password)
        if success:
            flash("您的密码已更新，请使用新密码登陆")
            return redirect(url_for('auth.login'))
        flash("密码重置失败")
    return render_template('auth/reset_password.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
