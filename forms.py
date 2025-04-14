from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators

class CompanyForm(FlaskForm):
    name = StringField('Osaühingu nimi', [
        validators.DataRequired(),
        validators.Length(min=3, max=100)
    ])
    register_number = StringField('Registrikood', [
        validators.DataRequired(),
        validators.Regexp(r'^\d{7}$', message="Registrikood peab olema 7 numbrit."),
    ])
  
    capital_size = IntegerField('Kogukapitali suurus eurodes', [
        validators.DataRequired(),
        validators.NumberRange(min=2500)
    ])
    submit = SubmitField('Create Company')

