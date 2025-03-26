from flask import Flask
from flask_restful import Resource, Api
from application.database import db

app = None
api = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizmasterdb.sqlite3"
    app.config["SECRET_KEY"] = "my_secret!"
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app,api

def create_admin():
    admin = Admin.query.first()
    if not admin:
        admin = Admin(id=1,username='admin12345@gmail.com',password='12345')
        db.session.add(admin)
        db.session.commit()

app,api = create_app()
from application.controllers import *

from application.api import *


if __name__ == "__main__":
    db.create_all()
    create_admin()
    app.run()