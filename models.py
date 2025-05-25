from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Perfil(db.Model):
    """
        Define los privilegios del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Integer, unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Perfil {self.nombre}>'

class Usuario(db.Model):
    """
        Actua con el sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)
    perfil = db.relationship('Perfil', backref='perfil', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'
    
class Extraccion(db.Model):
    """
        Registra datos sobre la extraccion realizada.
    """
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    descripcion = db.Column(db.String(200), nullable=True)
    usuario = db.relationship('Usuario', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Extraccion {self.fecha}>'
    
class Registro(db.Model):
    """
        Contiene informacion sobre una operacion en el punto de venta.
    """
    id = db.Column(db.Integer, primary_key=True)
    num_nota = db.Column(db.String(100), nullable = False)
    folio = db.Column(db.String(100), nullable=False)
    tienda = db.Column(db.String(100), nullable=True)
    fecha_vencimiento = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(25), nullable=True)
    total = db.Column(db.Float, nullable=False)
    abonado = db.Column(db.Float, nullable=False)
    debe = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    extraccion = db.relationship('Extraccion', backref='extraccion', lazy=True)

    def __repr__(self):
        return f'<Registro {self.folio}>'
