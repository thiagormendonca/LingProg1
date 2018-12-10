from flask import render_template, request, redirect, url_for
from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Horario, Agendamento
from werkzeug.urls import url_parse
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
        horario = Horario.query.filter_by(hora=horarioselecionado[:2]).first()
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
            if hora.minuto == 0:
                minuto = '00'
            else:
                minuto = str(hora.minuto)
            agends = agends + [ { 'dre': user.dre, 'horario': str(hora.hora) + ":" + minuto }]
        agorah = datetime.datetime.now().hour
        agoram = datetime.datetime.now().minute
        msg = 0
        if agoram > 0:
            h = Horario.query.all()
            for i in h:
                if i.hora > agorah:
                    h.remove(i)
            if h is None:
                msg = 0
            else:
                a = 0
                for i in h:
                    a = a + Agendamento.query.filter_by(horario_id=i.id).count()
                msg = a
        return render_template('admin.html', agends=agends, msg=msg)
    else:
        userdre = request.args.get('dre')
        user = User.query.filter_by(dre=userdre).first()
        db.session.delete(Agendamento.query.filter_by(user_id=user.id).first())
        db.session.commit()
        return redirect('/admin')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
