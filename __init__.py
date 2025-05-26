from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy() # Instancia de SQLAlchemy, sin pasar la app aquí
migrate = Migrate() # Instancia de Flask-Migrate

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Cargar configuraciones (ej. desde config.py)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy con la aplicación
    db.init_app(app)
    migrate.init_app(app, db) # Inicializar Flask-Migrate

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from models import User, Profile, Extraccion, Registro

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importar y registrar Blueprints
    from endpoints.auth import auth_route

    app.register_blueprint(auth_route, url_prefix='/auth')

    return app