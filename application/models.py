from .database import db
from zoneinfo import ZoneInfo
from datetime import datetime


def get_local_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))
    

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, default=1)
    username = db.Column(db.String(50), unique=True, nullable=False, default='admin123')
    password = db.Column(db.String(50), nullable=False, default='admin@123')

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable = False)
    full_name = db.Column(db.String(50), nullable = False)
    qualification = db.Column(db.String)
    dob = db.Column(db.Date)

    quizes = db.relationship('Quiz', secondary='users_quizes', back_populates='users')
    scores = db.relationship('Score', backref='users', lazy=True, cascade='all, delete')

class Subject(db.Model):
    __tablename__='subjects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique = True, nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship('Chapter', backref='subjects', lazy=True, cascade='all, delete-orphan')

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique = True, nullable=False)
    description = db.Column(db.Text)

    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    questions = db.relationship('Question', backref='chapters', lazy=True, cascade='all, delete-orphan')
    quizes = db.relationship('Quiz', backref='chapters', lazy=True, cascade='all, delete-orphan')
    
class Quiz(db.Model):
    __tablename__ = 'quizes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=True)
    time_duration = db.Column(db.String, nullable=True)
    remarks = db.Column(db.Text, nullable=True)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)

    users = db.relationship('User', secondary='users_quizes', back_populates='quizes')
    questions = db.relationship('Question', backref='quizes', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quizes', lazy=True, cascade='all, delete-orphan')


class UserQuiz(db.Model):
    __tablename__ = 'users_quizes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), primary_key=True, nullable=False)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String, nullable=False)
    option_b = db.Column(db.String, nullable=False)
    option_c = db.Column(db.String, nullable=False)
    option_d = db.Column(db.String, nullable=False)
    correct_option =db.Column(db.String, nullable=False)
    
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable=False)

class Score(db.Model):
    __tablename__='scores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_scored = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=get_local_time)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable=False)








        
