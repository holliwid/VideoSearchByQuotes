from flask import Flask, flash, render_template, request, redirect
from busnesLogic import search_quote
import forms
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    search = forms.QuotesSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search_quote(search.data['search'])
    results = search_quote(search.data['search'])

    if results == []:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('results.html', results=results, form=search)

@app.route('/dada')
def dada():
    search = forms.QuotesSearchForm(request.form)
    render_template('index.html', form=search)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'


    app.run()