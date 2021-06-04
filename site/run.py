#!flask/bin/python
from main import app

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.run(debug=True)