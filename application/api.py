from flask_restful import Resource
from flask import jsonify
from app import api

from .models import *

class SubjectsResource(Resource):
    def get(self):
        subjects = Subject.query.all()
        if subjects:
            return jsonify([{'id':s.id,'name':s.name,'description':s.description} for s in subjects])
        else:
            return "None"
    
class ChaptersResource(Resource):
    def get(self):
        chapters = Chapter.query.all()
        if chapters:
            return jsonify([{'id':c.id,'name':c.name,'description':c.description,'subject_id':c.subject_id} for c in chapters])
        else:
            return "None"

class QuizResource(Resource):
    def get(self):
        quizes = Quiz.query.all()
        if quizes:
            return jsonify([{'id':q.id,'title':q.title,'date_of_quiz':q.date_of_quiz,'time_duration':q.time_duration,'remarks':q.remarks,'chapter_id':q.chapter_id} for q in quizes])
        else:
            return "None"
    
class ScoreResource(Resource):
    def get(self):
        scores = Score.query.all()
        if scores:
            return jsonify([{'id':s.id,'total_scored':s.total_scored,'timestamp':s.timestamp,'user_id':s.user_id,'quiz_id':s.quiz_id} for s in scores])
        else:
            return "None"
        

api.add_resource(SubjectsResource,'/api/subjects')
api.add_resource(ChaptersResource,'/api/chapters')
api.add_resource(QuizResource,'/api/quizzes')
api.add_resource(ScoreResource,'/api/scores')