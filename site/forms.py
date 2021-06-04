from wtforms import Form, StringField, SelectField

class QuotesSearchForm(Form):
    search = StringField('')