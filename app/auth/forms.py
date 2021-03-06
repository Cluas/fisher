from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo

from .models import User


class RegisterForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(8, 64),
        Email(message='电子邮箱不符合规范')
    ])

    password = PasswordField(validators=[
        DataRequired(message='密码不可为空, 请输入您的密码'),
        Length(6, 32)
    ])

    nickname = StringField(validators=[
        DataRequired(),
        Length(2, 10, message='昵称至少需要2个字符, 至多10个字符')
    ])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(8, 64),
        Email(message='电子邮箱不符合规范')
    ])

    password = PasswordField(validators=[
        DataRequired(message='密码不可为空, 请输入您的密码'),
        Length(6, 32)
    ])


class EmailForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(8, 64),
        Email(message='电子邮箱不符合规范')
    ])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message="密码长度至少需要在6到32个字符之间"),
        EqualTo('password2', message='两次输入的密码不相同')
    ])
    password2 = PasswordField(validators=[
        DataRequired(),
        Length(3, 32)
    ])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField(validators=[DataRequired()])
