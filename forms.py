from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError

# Formulario para agregar/editar productos
class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=1, max=100, message="El nombre debe tener entre 1 y 100 caracteres.")
        ]
    )
    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=0, message="La cantidad debe ser 0 o mayor.")
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
    submit = SubmitField("Guardar")

    # Validación personalizada del campo nombre
    def validate_nombre(self, field):
        if field.data is None or str(field.data).strip() == "":
            raise ValidationError("El nombre no puede quedar vacío.")
        field.data = str(field.data).strip()
