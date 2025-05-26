from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from models import Usuario, Perfil
from models import db

class RegistroForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    
    perfiles = QuerySelectMultipleField(
        'Perfil',
        query_factory=lambda: db.session.query(Perfil).order_by(Perfil.nombre),
        get_label='nombre',
        blank_text="Seleccionar perfiles..."
    )

    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor elige otro.')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese correo electrónico ya está registrado. Por favor elige otro.')