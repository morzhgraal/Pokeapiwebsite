from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from parse import find_pokemon, RequestsJSONDecodeError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Welcome to the PokeWiki!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or url_for("index"))
        flash("Неверная пара логин/пароль", "error")
    return render_template('autorisation.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают", "error")
            return render_template('registration.html', title='Регистрация',
                                   form=form)

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Такой пользователь уже есть', 'error')
            return render_template('registration.html', title='Регистрация',
                                   form=form)
        user = User(
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/find_poke', methods=['GET', 'POST'])
@login_required
def find_poke():
    try:
        pokemon = find_pokemon(request.form.get('search_poke'))
        name = list(pokemon.values())[0]
        if pokemon:
            return render_template('find_pokemon.html', pokemon=pokemon, name=name)
        return render_template('find_pokemon.html', pokemon='')
    except RequestsJSONDecodeError:
        return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена'), 404


def main():
    db_session.global_init("db/poke_api.db")
    app.run(port=5000)


if __name__ == '__main__':
    main()
