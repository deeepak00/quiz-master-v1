from flask import Flask, render_template, request, url_for, redirect,session
from flask import current_app as app
from datetime import datetime
import matplotlib.pyplot as plt


from .models import *



@app.route("/", methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        type = request.form.get('type')
        if type=="admin":
            admin = Admin.query.first()
            if admin:
                if (admin.username==username and admin.password==password):
                    return redirect('/admin_dash')
                return render_template('wrong_admin_credentials.html')
            return render_template('not_exist.html', msgto='admin')
        if type=="user":
            user = User.query.filter(User.username==username).first()
            if user:
                if user.password==password:
                    return redirect(f'/user_dash/{user.id}')
                return render_template('wrong_user_credentials.html')
            return render_template('not_exist.html', msgto='user')
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date() 

        exist = User.query.filter(User.username==username).first()
        if not exist:
            new_user = User(username=username,password=password,full_name=full_name,qualification=qualification,dob=dob)
            db.session.add(new_user)
            db.session.commit()
            return 'Registration Successfull. Now login'
        return 'Already Exist username. Try registreing with New username'
    return render_template("register.html")


@app.route('/admin_dash', methods=['GET','POST'])
def admin_dash():
    subjects = Subject.query.all()
    return render_template("admin_dash.html", subjects=subjects)

@app.route('/add_subject', methods=['GET','POST'])
def add_subject():
    if request.method=='POST':
        action = request.form.get('action')
        if action=='Save':
            name = request.form.get('name')
            description = request.form.get('description')
            new_subject = Subject(name=name,description=description)
            db.session.add(new_subject)
            db.session.commit()
            return redirect('/admin_dash')
        if action=='Cancel':
            return redirect('/admin_dash')
    return render_template('add_subject.html')

@app.route('/<int:subject_id>/delete', methods=['GET','POST'])
def delete_subject(subject_id):
    subject = Subject.query.filter(Subject.id==subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect("/admin_dash")

@app.route('/<int:subject_id>/edit', methods=['GET','POST'])
def edit_subject(subject_id):
    subject = Subject.query.filter(Subject.id==subject_id).first()
    if subject:
        if request.method=='POST':
            action = request.form.get('action')
            if action=="Save":
                subject.name = request.form.get('name')
                subject.description = request.form.get('description')
                db.session.commit()
                return redirect("/admin_dash")
            if action=="Cancel":
                return redirect('/admin_dash')
        return render_template('update_subject.html',subject=subject)
    return "No subject with this id"
    
@app.route("/user_read/<int:user_id>")
def user_read(user_id):
    user = User.query.filter(User.id==user_id).first()
    quizes = user.quizes
    return render_template('read_user.html', user=user, quizes=quizes)

@app.route("/subject_read/<int:subject_id>")
def subject_read(subject_id):
    subject = Subject.query.filter(Subject.id==subject_id).first()
    return render_template("read_subject.html",subject=subject)




@app.route('/add_chapter/<int:subject_id>', methods=['GET','POST'])
def add_chapter(subject_id):
    subject = Subject.query.filter(Subject.id==subject_id).first()
    if subject:
        if request.method=='POST':
            action = request.form.get('action')
            if action=='Save':
                id = subject.id
                name = request.form.get('c_name')
                description = request.form.get('description')
                new_chapter = Chapter(name=name,description=description,subject_id=id)
                db.session.add(new_chapter)
                db.session.commit()
                return redirect('/admin_dash')
            if action=='Cancel':
                return redirect('/admin_dash')
        return render_template('add_chapter.html',subject = subject)
    return "no subject with this ID"


@app.route('/admin_dash/<int:chapter_id>/delete', methods=['GET','POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.filter(Chapter.id==chapter_id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect('/admin_dash')

@app.route('/admin_dash/<int:chapter_id>/edit', methods=['GET','POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.filter(Chapter.id==chapter_id).first()
    if chapter:
        if request.method=='POST':
            action = request.form.get('action')
            if action=="Save":
                chapter = Chapter.query.filter(Chapter.id==chapter_id).first()
                chapter.name = request.form.get('c_name')
                chapter.description = request.form.get('description')
                db.session.commit()
                return redirect('/admin_dash')
            if action=="Cancel":
                return redirect('/admin_dash')
        return render_template('update_chapter.html',chapter=chapter)
    return "No chapter with this chapter ID"


@app.route("/chapter_read/<int:chapter_id>")
def chapter_read(chapter_id):
    chapter = Chapter.query.filter(Chapter.id==chapter_id).first()
    return render_template("read_chapter.html",chapter=chapter)




@app.route('/admin_quiz', methods=['GET','POST'])
def admin_quiz():
    quizs = Quiz.query.all()
    return render_template('admin_quiz.html',quizs=quizs)


@app.route('/add_quiz', methods=['GET','POST'])
def add_quiz():
    if request.method=='POST':
        action = request.form.get("action")
        if action=="Save":
            title = request.form.get('name')
            doq = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date() 
            duration = request.form.get('duration')
            remark = request.form.get('remark')
            chapter_id = request.form.get('c_id')
            exist = Quiz.query.filter(Quiz.title==title).first()
            if not exist:
                new_quiz = Quiz(title=title,date_of_quiz=doq,time_duration=duration,remarks=remark,chapter_id=chapter_id)
                db.session.add(new_quiz)
                db.session.commit()
                return redirect('/admin_quiz')
            return "Quiz Name Already Exist"
        if action=="Cancel":
            return redirect("/admin_quiz")
    return render_template('add_quiz.html',chapters= Chapter.query.all())

@app.route('/quiz/<int:quiz_id>/delete', methods=['GET','POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.filter(Quiz.id==quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    return redirect('/admin_quiz') 


@app.route('/quiz/<int:quiz_id>/edit', methods=['GET','POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.filter(Quiz.id==quiz_id).first()
    if quiz:
        if request.method=='POST':
            action = request.form.get('action')
            if action=="Save":
                quiz.date_of_quiz = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date() 
                quiz.time_duration = request.form.get('duration')
                quiz.remarks = request.form.get('remark')
                db.session.commit()
                return redirect("/admin_quiz")
            if action=="Cancel":
                return redirect("/admin_quiz")
        return render_template('update_quiz.html',quiz=quiz)
    return "Quiz with this ID is not exist"
    

@app.route("/quiz_read/<int:quiz_id>")
def quiz_read(quiz_id):
    quiz = Quiz.query.filter(Quiz.id==quiz_id).first()
    return render_template("read_quiz.html",quiz=quiz)





@app.route('/add_question/<int:quiz_id>', methods=['GET','POST'])
def add_question(quiz_id):
    quizz = Quiz.query.filter(Quiz.id==quiz_id).first()
    if quizz:
        if request.method=='POST':
            action = request.form.get('action')
            if action=="Save":
                title = request.form.get('qntitle')
                question = request.form.get('question')
                option_a = request.form.get('op1')
                option_b = request.form.get('op2') 
                option_c = request.form.get('op3')
                option_d = request.form.get('op4')
                correct_option = request.form.get('rop')
                chapter_id = quizz.chapter_id
                quiz_id = quizz.id

                new_question = Question(title=title,question=question,option_a=option_a,option_b=option_b,option_c=option_c,option_d=option_d,correct_option=correct_option,chapter_id=chapter_id,quiz_id=quiz_id)

                db.session.add(new_question)
                db.session.commit()
                return redirect('/admin_quiz')
            if action=="Close":
                return redirect('/admin_quiz')
        return render_template('add_question.html',quiz=quizz)
    return "No quiz with this quiz id"

@app.route('/question/<int:question_id>/delete', methods=['GET','POST'])
def delete_question(question_id):
    question = Question.query.filter(Question.id==question_id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect('/admin_quiz')


@app.route('/question/<int:question_id>/edit', methods=['GET','POST'])
def edit_question(question_id):
    question = Question.query.filter(Question.id==question_id).first()
    if question:
        if request.method=='POST':
            action = request.form.get('action')
            if action=="Save":
                question.question = request.form.get('question')
                question.option_a = request.form.get('op1')
                question.option_b = request.form.get('op2')
                question.option_c = request.form.get('op3')
                question.option_d = request.form.get('op4')
                question.correct_option = request.form.get('rop')
                db.session.commit()
                return redirect('/admin_quiz')
            if action=="Close":
                return redirect('/admin_quiz')
        return render_template('update_question.html',question=question)
    return "No Question with this question ID"
    
@app.route("/question_read/<int:question_id>")
def question_read(question_id):
    question = Question.query.filter(Question.id==question_id).first()
    return render_template("read_question.html",question=question)


