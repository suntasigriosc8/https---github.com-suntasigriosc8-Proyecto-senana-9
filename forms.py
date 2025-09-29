from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, NumberRange, Length, Email, ValidationError

class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=1, max=100, message="El nombre debe tener entre 1 y 100 caracteres.")
        ]
    )
    precio = DecimalField(
        "Precio",
        places=2,
        rounding=None,
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0, message="El precio debe ser 0.00 o mayor.")
        ]
    )
    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock debe ser 0 o mayor.")
        ]
    )
    imagen = FileField("Imagen del producto")
    submit = SubmitField("Guardar")

class RegisterForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio.")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio."),
            Email(message="Ingresa un email válido.")
        ]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria.")
        ]
    )
    submit = SubmitField("Registrar")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio."),
            Email(message="Ingresa un email válido.")
        ]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria.")
        ]
    )
    submit = SubmitField("Iniciar Sesión")
