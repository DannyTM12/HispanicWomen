from flask import render_template,Blueprint

from forms import RegistroForm

# creamos acceso a usuarios

auth_route= Blueprint('auth', __name__, url_prefix='/auth')

@auth_route.route('/')
def root():
    return render_template("auth/login.html")

@auth_route.route('/registrar')
def registrar_usuario():

    form = RegistroForm()

    return render_template("auth/registro.html", form=form)