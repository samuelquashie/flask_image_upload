from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField,StringField
from wtforms.validators import DataRequired

class ImageFile(FlaskForm):
    lname = StringField('Last  Name',validators=[DataRequired()])
    fname = StringField('First Name',validators=[DataRequired()])
    image = FileField('Upload Image')
    submit = SubmitField('Upload Image')