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
    
    
    
@app.route('/admin_summary')
def summary():
    total_user = User.query.count()  # Get total users efficiently
    if total_user == 0:
        total_user = 1  # Avoid division by zero
    
    sub_maxscore_dict = {}
    sub_usercount_dict = {}

    subjects = Subject.query.all()
    for subject in subjects:
         # Reset for each subject
        sub_user = 0 
        sub_maxscore = 0
        total_questions = 1  # Default to 1 to avoid division by zero

        for chapter in subject.chapters:
            for quiz in chapter.quizes:
                if quiz.scores and quiz.questions:  # Check if scores and questions exist
                    max_quiz_score = max(score.total_scored for score in quiz.scores)
                    num_questions = len(quiz.questions)  # Total number of questions in the quiz

                    if max_quiz_score > sub_maxscore:
                        sub_maxscore = max_quiz_score
                        total_questions = num_questions

                    for _ in quiz.users:  # Count users who took this quiz
                        sub_user += 1

        sub_usercount_dict[subject.name] = round(min((sub_user / total_user) * 100, 100), 2)
        sub_maxscore_dict[subject.name] = round(min((sub_maxscore / total_questions) * 100, 100), 2)


    if sub_usercount_dict:
        generate_subject_attempt_by_user(sub_usercount_dict)

    if sub_maxscore_dict:
        generate_subject_top_scores_chart(sub_maxscore_dict)

    return render_template('admin_summary.html',sub_usercount_dict=sub_usercount_dict)


def generate_subject_attempt_by_user(data):
    labels = list(data.keys())
    sizes = list(data.values())

    plt.figure(figsize=(3,2))

    plt.bar(labels,sizes,color='black')
    plt.xlabel('subjects')
    plt.ylabel('percentage attempt')
    plt.xticks(rotation=20)
    plt.ylim(0,100)

    for i, v in enumerate(sizes):
        plt.text(i, v+1, str(v)+" %", ha='center', fontsize=5)

    plt.grid(axis='y',linestyle='--',alpha=0.2)

    plt.title("Subject wise attempting percentage")

    plt.savefig("static/subject_attempt_percentage.png", dpi=140, bbox_inches="tight")
    plt.close()

def generate_subject_top_scores_chart(sub_maxscore_dict):
    subjects = list(sub_maxscore_dict.keys())  # X-axis (Subjects)
    scores = list(sub_maxscore_dict.values())  # Y-axis (Scores)

    plt.figure(figsize=(3,2))

    # All bars will be black
    plt.bar(subjects, scores, color='black')

    plt.xlabel("Subjects")
    plt.ylabel("Top Score")
    plt.title("Subject Wise Top Scores")
    plt.xticks(rotation=20)  # Rotate labels for readability
    plt.ylim(0,100)

    for i, v in enumerate(scores):
        plt.text(i, v+1, str(v)+" %", ha='center', fontsize=5)

    
    plt.grid(axis='y', linestyle='--', alpha=0.2)

    # Save the chart in 'static' folder
    plt.savefig("static/subject-top-scores.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    

@app.route("/search", methods=['POST'])
def search():
    string = request.form.get('string')
    field = request.form.get('field')
    if not string:
        return 'Please Enter something to serch'
    results=[]
    if field=="users":
        if string=="*":
            results = User.query.all()
        else:
            results = User.query.filter(User.username.ilike(f'%{string}%')).all()
    elif field=="chapters":
        if string=="*":
            results = Chapter.query.all()
        else:
            results = Chapter.query.filter(Chapter.name.ilike(f'%{string}%')).all()
    elif field=="subjects":
        if string=="*":
            results = Subject.query.all()
        else:
            results = Subject.query.filter(Subject.name.ilike(f'%{string}%')).all()
    elif field=="quizes":
        if string=="*":
            results = Quiz.query.all()
        else:
            results= Quiz.query.filter(Quiz.title.ilike(f'%{string}%')).all()
    elif field=="questions":
        if string=="*":
            results = Question.query.all()
        else:
            results = Question.query.filter(Question.question.ilike(f'%{string}%')).all()
    
    return render_template('search.html', results=results,field=field,string=string)
    
    
    



@app.route('/user_dash/<int:user_id>', methods=['GET','POST'])
def user_dash(user_id):
    user = User.query.filter(User.id==user_id).first()
    quizes = Quiz.query.order_by(Quiz.id.desc()).all()
    userquiz = UserQuiz.query.all()
    attempted = [(i.user_id, i.quiz_id) for i in userquiz]
    return render_template("user_dash.html",user=user,quizes=quizes,attempted=attempted)
    

@app.route('/user_quizview/<int:user_id>/<int:quiz_id>', methods=['GET','POST'])
def user_quizview(user_id,quiz_id):
    if request.method=='POST':
        return redirect(f'/user_dash/{user_id}')
    quiz = Quiz.query.filter(Quiz.id==quiz_id).first()
    chapter = quiz.chapters
    subject = chapter.subjects
    return render_template('user_quizview.html',quiz=quiz,chapter=chapter,subject=subject,user_id=user_id)
    

@app.route('/user_score/<int:user_id>', methods=['GET','POST'])
def user_score(user_id):
    user = User.query.filter(User.id==user_id).first()
    quizes = user.quizes
    return render_template('user_score.html',user = user, quizes=quizes)


@app.route("/user_summary/<int:user_id>", methods=['GET','POST'])
def user_summary(user_id):
    subjectwise_no_of_quiz = {}
    subjectwise_score = {}
    total_number_of_quiz = 0
    subjects = Subject.query.all()
    user = User.query.filter(User.id==user_id).first()
    quiz = Quiz.query.all()
    for i in quiz:
        total_number_of_quiz+=1
    quizes = user.quizes
    for quiz in quizes:
        chapter = Chapter.query.filter(Chapter.id==quiz.chapter_id).first()
        subject = Subject.query.filter(Subject.id==chapter.subject_id).first()

        if subject.name not in subjectwise_no_of_quiz:
            subjectwise_no_of_quiz[subject.name]=1
        else:
            subjectwise_no_of_quiz[subject.name]+=1
        
        total_score = sum([i.total_scored for i in quiz.scores])
        no_of_ques = sum([1 for _ in quiz.questions])
        if subject.name not in subjectwise_score:
            subjectwise_score[subject.name]=total_score/no_of_ques
        else:
            subjectwise_score[subject.name]+=total_score/no_of_ques

    for x in subjectwise_score:
        subjectwise_score[x] = round((subjectwise_score[x]/subjectwise_no_of_quiz[x])*100,2)
 
    for x in subjects:
        if x.name not in subjectwise_no_of_quiz:
            subjectwise_no_of_quiz[x.name]=0
        if x.name not in subjectwise_score:
            subjectwise_score[x.name]=0
    

    
    subject_wise_quiz_chart(subjectwise_no_of_quiz,total_number_of_quiz)
    subjectwise_score_chart(subjectwise_score)

    return render_template('user_summary.html',user=user)

def subjectwise_score_chart(data):
    subjects = list(data.keys())  # X-axis (Subjects)
    score = list(data.values())  # Y-axis (Scores)

    plt.figure(figsize=(3,2))

    # All bars will be black
    plt.bar(subjects, score, color='black')

    plt.xlabel("Subjects")
    plt.ylabel("Average marks  ")
    plt.title("Subject wise avg. Marks")
    plt.xticks(rotation=20)  # Rotate labels for readability
    plt.ylim(0,100)
    

    for i, v in enumerate(score):
        plt.text(i, v+0.5, str(v)+"%", ha='center', fontsize=5)

    
    plt.grid(axis='y', linestyle='--', alpha=0.2)

    # Save the chart in 'static' folder
    plt.savefig("static/subjectwise-score.png", dpi=150, bbox_inches='tight')
    plt.close()



def subject_wise_quiz_chart(data,total):
    subjects = list(data.keys())  # X-axis (Subjects)
    count = list(data.values())  # Y-axis (Scores)

    plt.figure(figsize=(3,2))

    # All bars will be black
    plt.bar(subjects, count, color='black')

    plt.xlabel("Subjects")
    plt.ylabel("No. of quizz attemped")
    plt.title("Subject wise number of quiz attempted")
    plt.xticks(rotation=20)  # Rotate labels for readability
    plt.ylim(0,total)
    

    for i, v in enumerate(count):
        plt.text(i, v+0.5, str(v), ha='center', fontsize=5)

    
    plt.grid(axis='y', linestyle='--', alpha=0.2)

    # Save the chart in 'static' folder
    plt.savefig("static/subject-wise-quiz-chart.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    

@app.route("/user_search/<int:user_id>", methods=['POST'])
def user_search(user_id):
        user = User.query.filter(User.id==user_id).first()
        string = request.form.get('string')
        field = request.form.get('field')
        if not string:
            return 'Please Enter something to search'
        results=[]
        if field=="chapters":
            if string=="*":
                results = Chapter.query.all()
            else:
                results = Chapter.query.filter(Chapter.name.ilike(f'%{string}%')).all()
        elif field=="subjects":
            if string=="*":
                results = Subject.query.all()
            else:
                results = Subject.query.filter(Subject.name.ilike(f'%{string}%')).all()
        elif field=="quizes":
            if string=="*":
                results = Quiz.query.all()
            else:
                results= Quiz.query.filter(Quiz.title.ilike(f'%{string}%')).all()
        
        return render_template('user_search.html', results=results,field=field,string=string,user=user)





@app.route("/user_subject_read/<int:user_id>/<int:subject_id>", methods=['GET','POST'])
def user_subject_read(user_id,subject_id):
    subject = Subject.query.filter(Subject.id==subject_id).first()
    user = User.query.filter(User.id==user_id).first()
    return render_template('user_subject_read.html', user=user, subject=subject)

@app.route("/user_chapter_read/<int:user_id>/<int:chapter_id>", methods=['GET','POST'])
def user_chapter_read(user_id,chapter_id):
    chapter = Chapter.query.filter(Chapter.id==chapter_id).first()
    user = User.query.filter(User.id==user_id).first()
    return render_template('user_chapter_read.html', user=user, chapter=chapter)

@app.route("/user_quiz_read/<int:user_id>/<int:quiz_id>", methods=['GET','POST'])
def user_quiz_read(user_id,quiz_id):
    quiz = Quiz.query.filter(Quiz.id==quiz_id).first()
    user = User.query.filter(User.id==user_id).first()
    return render_template('user_quiz_read.html', user=user, quiz=quiz)
    
    
@app.route("/quiz_handle/<int:user_id>/<int:quiz_id>", methods=['GET','POST'])
def quiz_handle(user_id, quiz_id):
    quiz = Quiz.query.filter(Quiz.id == quiz_id).first()
    user = User.query.filter(User.id == user_id).first()

    exist1 = UserQuiz.query.filter(UserQuiz.user_id==user_id,UserQuiz.quiz_id==quiz_id).first()

    if not exist1:
        user.quizes.append(quiz)
        db.session.commit()

    exist2 = Score.query.filter(Score.user_id==user.id, Score.quiz_id==quiz.id).first()
    if not exist2:
        score = Score(total_scored=0,user_id=user.id,quiz_id=quiz.id)
        db.session.add(score)
        db.session.commit()

    questions = quiz.questions
    total_scored = 0
    if request.method == 'POST':
        for question in questions:
            if request.form.get(f'{question.id}') == question.correct_option:
                total_scored += 1
        score = Score.query.filter(Score.user_id==user.id, Score.quiz_id==quiz.id).first()
        score.total_scored = total_scored
        db.session.commit()
        return render_template('user_result.html', user=user, quiz = quiz , total_scored = total_scored)
    
    hh, mm = map(int, quiz.time_duration.split(":"))
    total_seconds = (hh * 3600) + (mm * 60)
    
    return render_template(
        'quiz_page.html',
        questions=questions,
        quiz=quiz,
        user=user,
        quiz_duration=total_seconds 
    )


