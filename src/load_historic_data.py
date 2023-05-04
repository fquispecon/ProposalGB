from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department=db.Column(db.String(100),unique=True)

    def __init__(self,id,department):
        self.id=id
        self.department=department