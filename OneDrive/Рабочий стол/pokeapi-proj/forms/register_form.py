from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email("Некорректный email")],
                        render_kw={"placeholder": "Enter your email"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password"})
    password_again = PasswordField(validators=[DataRequired()],
                                   render_kw={"placeholder": "Repeat your password"})
    submit = SubmitField('REGISTER')
