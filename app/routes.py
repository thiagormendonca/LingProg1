from flask import render_template, request, redirect
from app import app

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        dre = request.form['DRE']
        senha = request.form['senha']
        if dre=='1180' and senha=='123':
            return redirect('/index')
        else:
            return render_template('login.html', msg='Informações incorretas!')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/index')
def index():
    return render_template('index.html')