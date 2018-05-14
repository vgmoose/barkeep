from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, URL, Optional

import os, re

pattern = re.compile("^\w+$")   # alphanumeric and underscore

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

class AddPackageForm(FlaskForm):
    name = StringField("Package Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    category = SelectField("Category", choices=[("game", "Games"), ("emu", "Emulators"), ("tool", "Tools"), ("concept", "Concepts"), ("loader", "Loaders")])
    version = StringField("Version", validators=[DataRequired()])
    short_desc = StringField("Short Description", validators=[DataRequired()])
    details = TextAreaField("Long Details", render_kw={'class': 'form-control', 'rows': 15})
    url = StringField("URL", validators=[URL()])
    license = StringField("License")


    submit = SubmitField('Create')
    	# "title": "AppStore NX",
    	# "author": "vgmoose",
    	# "category": "loader",
    	# "version": "1.0",
    	# "description": "Download and manage homebrew apps",
    	# "details": "The Homebrew App Store NX is graphical frontend to the get package manager for downloading and managing homebrew on the Nintendo Switch. This is a successor to the Wii U Homebrew App Store.\\n\\nFor further information you can visit the Source link below or browse to the GBAtemp release post here : https://gbatemp.net/threads/switch-homebrew-appstore.493086/\\n",
    	# "url": "https://github.com/vgmoose/appstorenx",
    	# "license": "GPLv3 License"

    def validate_name(self, field):
        if not re.match(pattern, field.data):
            raise ValidationError("Package name must be alphanumeric, with no spaces")
