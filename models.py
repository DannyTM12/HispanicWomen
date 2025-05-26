from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from __init__ import db

# Tabla intermedia para la relación muchos-a-muchos entre User y Profile
user_profiles = Table('user_profiles', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('profile_id', Integer, ForeignKey('profile.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """
        Registra la informacion de quien usa el app.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # <--- Cambiar a password_hash
    email = db.Column(db.String(120), unique=True, nullable=False)
    profiles = relationship('Profile', secondary=user_profiles, backref='users', lazy='dynamic')

    extracciones = relationship('Extraccion', backref='usuario', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Profile(db.Model):
    """
        Define los privilegios del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Profile {self.name}>'

class Extraccion(db.Model):
    """
        Registra datos sobre la extraccion realizada.
    """
    __tablename__ = 'extraccion'  # Added tablename
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    fecha_extraccion = db.Column(db.DateTime, nullable=False, default=datetime.now())

    usuario_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False) # Referencia al ID del usuario

    def __repr__(self):
        return f'<Extraccion {self.nombre_archivo} por {self.usuario_id}>'

class Registro(db.Model):
    """
        Contiene informacion sobre una operacion en el punto de venta.
    """
    __tablename__ = 'registro'  # Added tablename
    id = db.Column(db.Integer, primary_key=True)
    num_nota = db.Column(db.String(100), nullable=False)
    folio = db.Column(db.String(100), nullable=False)
    tienda = db.Column(db.String(100), nullable=True)
    fecha_vencimiento = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(25), nullable=True)
    total = db.Column(db.Float, nullable=False)
    abonado = db.Column(db.Float, nullable=False)
    debe = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    extraccion_id = db.Column(db.Integer, db.ForeignKey('extraccion.id'), nullable=True)  # Added foreign key
    extraccion = db.relationship('Extraccion', backref='registros', lazy=True)  # Changed backref name

    def __repr__(self):
        return f'<Registro {self.folio}>'