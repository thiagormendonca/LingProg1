from flask import render_template, request, redirect, url_for
from app import app, db
from flask_login import current_user, login_user, login_required
from app.models import User, Horario, Agendamento
import datetime

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/home')
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
                next_page = url_for('home')
            return redirect(next_page)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/home')
        else:
            return render_template('cadastro.html')
    else:
        usuario = request.form['user']
        email = request.form['email']
        dre = request.form['DRE']
        senha = request.form['pass']
        user = User(usuario=usuario, email=email, dre=dre, admin=0)
        user.set_password(senha)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/agendamento', methods=['GET', 'POST'])
@login_required
def agendamento():
    if request.method == 'GET':
        return render_template('agendamento.html')
    else:
        checaagend = Agendamento.query.filter_by(user_id=current_user.id).first()
        if not checaagend is None:
            return render_template('agendamento.html', msg='Você já agendou!') 
        horarioselecionado = request.form['horario']
        horario = Horario.query.filter_by(horario=horarioselecionado).first()
        horario.removeVaga()
        agendamento = Agendamento(user_id=current_user.id, horario_id=horario.id)
        db.session.add(agendamento)
        db.session.commit()
        return render_template('agendamento.html', msg='Agendado com sucesso!')

@app.route('/admin')
@login_required
def admin():
    if request.args.get('dre') is None:
        agendamentos = Agendamento.query.all()
        agends = []
        for a in agendamentos:
            user = User.query.filter_by(id=a.user_id).first()
            hora = Horario.query.filter_by(id=a.horario_id).first()
            agends = agends + [ { 'dre': user.dre, 'horario': hora.horario }]
        agora = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
        msg = 0
        if datetime.datetime.now().minute > 0:
            h = Horario.query.filter_by(horario=str(datetime.datetime.now().hour) + ':00').first()
            if h is None:
                msg = 0
            else:
                a = Agendamento.query.filter_by(horario_id=h.id)
                msg = len(a)
        return render_template('admin.html', agends=agends, msg=msg)
    else:
        userdre = request.args.get('dre')
        user = User.query.filter_by(dre=userdre).first()
        db.session.delete(Agendamento.query.filter_by(user_id=user.id).first())
        db.session.commit()
        return redirect('/admin')
