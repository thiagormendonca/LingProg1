from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dre = db.Column(db.String(9), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Integer, index=True) #Se for 1, admin, se 0 nao

    def __repr__(self):
        return '<User {}>'.format(self.usuario)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def setAdmin(self):
        self.admin = 1
    
    def removeAdmin():
        self.admin = 0

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(64))
    quantidade = db.Column(db.Integer)

    def __repr__(self):
        return '<Horario {}>'.format(self.horario)

    def removeVaga(self):
        self.quantidade = self.quantidade - 1

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'))

    def __repr__(self):
        return '<Agendamento {}>'.format(self.horario_id)