from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from wtforms.validators import DataRequired

class ImageFile(FlaskForm):
    image = FileField('Upload Image')
    submit = SubmitField('Upload Image')