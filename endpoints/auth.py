from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user 
from forms import RegistroForm, LoginForm

from models import User, Profile
from __init__ import db

# creamos acceso a usuarios

auth_route = Blueprint('auth', __name__, url_prefix='/auth')

@auth_route.route('/')
def root():
    return render_template("auth/login.html")

@auth_route.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    form = RegistroForm()
    form.profiles.choices = [(p.id, p.name) for p in Profile.query.order_by(Profile.name).all()]

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data # Contraseña en texto plano del formulario
        selected_profile_ids = form.profiles.data

        new_user = User(username=username, email=email)
        new_user.set_password(password) # <--- Usar el nuevo método set_password

        for profile_id in selected_profile_ids:
            profile = Profile.query.get(profile_id)
            if profile:
                new_user.profiles.append(profile)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'¡Cuenta creada exitosamente para {username}! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')

    return render_template('auth/registro.html', title='Registro', form=form)


@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth.dashboard'))
        else:
            flash('Inicio de sesión fallido. Por favor, revisa tu nombre de usuario y contraseña.', 'danger')
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)


@auth_route.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('root'))


@auth_route.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard', user=current_user)