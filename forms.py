from flask_wtf import FlaskForm
import re
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, url, ValidationError
from werkzeug.datastructures import MultiDict

def validatePostURL(form, field):
	url_regex = r"(^(http|https):\/\/www\.instagram\.com\/p\/.*)"
	regex = re.compile(url_regex)
	if regex.match(field.data) is None:
		raise ValidationError("Your URL should start with https://instagram/p/")

class InstagramVideoURLDecoder(FlaskForm):

	videoURL = StringField('Instagram Video URL',
		validators=[DataRequired(),
			validatePostURL,
			Length(min=2, max=100),
			url(message='Please make sure you enter a valid URL',
			require_tld=True)])

	submit = SubmitField('Obtener video')

	def reset(self):
		blankData = MultiDict()
		self.process(blankData)