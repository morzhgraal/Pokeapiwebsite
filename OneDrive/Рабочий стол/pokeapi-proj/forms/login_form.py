from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email("Некорректный email")],
                        render_kw={"placeholder": "Enter your email"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Repeat your password"})
    remember_me = BooleanField('Remember me here')
    submit = SubmitField('LOGIN')
