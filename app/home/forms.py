from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

import os
DATA = "./data/"

class AddRepoForm(FlaskForm):
    """
    Form for creating a new repo
    (makes a folder on disk)
    """
    name = StringField('Folder name', validators=[DataRequired()])
    
    submit = SubmitField('Create')

    def validate_name(self, field):
        if field.data.lower() == "add":
            raise ValidationError("Folder name cannot be 'add'")
        if os.path.isdir(DATA + field.data.lower()):
            raise ValidationError("A repo with that name already exists")
