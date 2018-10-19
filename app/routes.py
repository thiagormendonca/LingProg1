from flask import render_template, request, redirect, url_for
from app import app, db
from flask_login import current_user, login_user, login_required
from app.models import User

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect('/index')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/index')
        else:
            return render_template('login.html')
    else:
        dre = request.form['DRE']
        senha = request.form['senha']
        user = User.query.filter_by(dre=dre).first()
        if user is None or not user.check_password(senha):
            return render_template('login.html', msg='DRE ou senha inválidos')
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/index')
        else:
            return render_template('cadastro.html')
    else:
        usuario = request.form['usuario']
        email = request.form['email']
        dre = request.form['DRE']
        senha = request.form['senha_1']
        user = User(username=usuario, email=email, dre=dre)
        user.set_password(senha)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')


@app.route('/index')
@login_required
def index():
    return render_template('index.html')
