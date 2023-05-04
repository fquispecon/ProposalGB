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

    def __init__(self,department):
        self.department=department

class Hired(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    datetime=db.Column(db.String(100))
    department_id=db.Column(db.Integer)
    job_id=db.Column(db.Integer)
    
    def __init__(self,name,datetime,department_id,job_id):
        self.name=name
        self.datetime=datetime
        self.department_id=department_id
        self.job_id=job_id

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job=db.Column(db.String(100),unique=True)

    def __init__(self,job):
        self.job=job

with app.app_context():
    db.create_all()


class DepartmentSchema(ma.Schema):
    class Meta:
        fields=('id','department')

class HiredSchema(ma.Schema):
    class Meta:
        fields=('id','name','datetime','department_id','job_id')

class JobSchema(ma.Schema):
    class Meta:
        fields=('id','job')


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

hire_schema = HiredSchema()
hires_schema = HiredSchema(many=True)

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

@app.route('/department',methods=['POST'])
def send_department():
    department=request.json['department']
    new_task=Departments(department)
    db.session.add(new_task)
    db.session.commit()
    return department_schema.jsonify(new_task)

@app.route('/hire',methods=['POST'])
def send_hire():
    name=request.json['name']
    datetime=request.json['datetime']
    department_id=request.json['department_id']
    job_id=request.json['job_id']

    new_task=Hired(name,datetime,department_id,job_id)
    db.session.add(new_task)
    db.session.commit()
    return hire_schema.jsonify(new_task)

@app.route('/job',methods=['POST'])
def send_job():
    job=request.json['job']

    new_task=Jobs(job)
    db.session.add(new_task)
    db.session.commit()
    return job_schema.jsonify(new_task)


if __name__=="__main__":
    app.run(debug=True)