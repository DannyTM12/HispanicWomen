from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------- Tabla Intermedia -------------------------

perfil_usuario = db.Table(
    'perfil_usuario',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('id_perfil', db.Integer, db.ForeignKey('perfil.id'), primary_key=True)
)

# ------------------------------- Modelos -------------------------------------

class Perfil(db.Model):
    """
        Asigna los privilegios del usuario.
    """
    __tablename__ = 'perfil'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

    usuarios = db.relationship("Usuario", secondary=perfil_usuario, back_populates="perfiles")  # Corrected name

    def __repr__(self):
        return f'<Perfil {self.nombre}>'

class Usuario(db.Model):
    """
        Actua con el sistema.
    """
    __tablename__ = 'usuario'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)

    perfiles = db.relationship("Perfil", secondary=perfil_usuario, back_populates="usuarios")  # Corrected name

    extracciones = db.relationship('Extraccion', back_populates='usuario')  # Corrected name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Extraccion(db.Model):
    """
        Registra datos sobre la extraccion realizada.
    """
    __tablename__ = 'extraccion'  # Added tablename
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now(), nullable=False, index=True)
    descripcion = db.Column(db.String(200), nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Added foreign key
    usuario = db.relationship('Usuario', back_populates='extracciones')  # Corrected name

    def __repr__(self):
        return f'<Extraccion {self.fecha}>'

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