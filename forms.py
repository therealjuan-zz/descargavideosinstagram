from flask_wtf import FlaskForm
import re
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, url, ValidationError
from werkzeug.datastructures import MultiDict

def validatePostURL(form, field):
	url_regex = r"(^(http|https):\/\/www\.instagram\.com\/p\/.*)"
	regex = re.compile(url_regex)
	if regex.match(field.data) is None:
		raise ValidationError("La dirección URL debe ser del estilo https://instagram/p/aB23dCeZ")

class InstagramVideoURLDecoder(FlaskForm):

	videoURL = StringField('URL del Post de Instagram',
		validators=[DataRequired(),
			validatePostURL,
			Length(min=2, max=100),
			url(message='Introduce una URL válida de Instagram',
			require_tld=True)])

	submit = SubmitField('Obtener video')

	def reset(self):
		blankData = MultiDict()
		self.process(blankData)