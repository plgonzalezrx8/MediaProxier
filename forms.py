from wtforms import StringField, validators, SubmitField
from flask_wtf import FlaskForm
class ImageLinkForm(FlaskForm):
	link = StringField('ImageLink')
	submit = SubmitField('Submit')
