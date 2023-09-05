from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import secretmanager
import json

app = Flask(__name__)

# GCP Secret Manager
client = secretmanager.SecretManagerServiceClient()
requests = "projects/104663039364/secrets/flaskcrudsecret/versions/1"
response = client.access_secret_version({"name":requests})
secret_dict = json.loads(response.payload.data.decode("utf-8"))

dbUsername = secret_dict["dbUsername"]
dbPassword = secret_dict["dbPassword"]
dbName = secret_dict["dbName"]
dbHost = secret_dict["dbHost"]
dbInstance = secret_dict["dbInstance"]
dbPort = 3306

# Mysq Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{dbUsername}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employees(db.Model):
    EmployeeID = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(5))
    Email = db.Column(db.String(120),unique=True,nullable=False)
    Department= db.Column(db.String(20),nullable=False)

app.app_context().push()
db.create_all()

@app.route('/ls', methods=['POST', 'GET'])
def listdb():
    data = Employees.query.all()
    if len(data) != 0:
        dbdict = {}
        dblist = []
        for i in data:
            dbdict['employeeid']= i.EmployeeID
            dbdict['Name'] = i.Name
            dbdict['Email'] = i.Email
            dbdict['Department'] = i.Department
            dblist.append(dbdict)
            dbdict = {}
        return jsonify(dblist)
    else:
        result = {"msg": "Employee data not found.", "status":"error"}
        return jsonify(result)

@app.route('/add', methods = ['POST', 'GET'] )
def add():
    data = request.get_json()
    # Validate duplicate email id
    emp_email_status = Employees.query.filter_by(Email=data['Email']).first()

    if  emp_email_status:
        result = {"msg":"Error: Duplicate user email id is not allowed","status":"error"}
        return jsonify(result)
    else:
        emp_db_connection = Employees(Name=data['Name'],Email=data['Email'],Department=data['Department'])
        db.session.add(emp_db_connection)
        db.session.commit()
        result = {"msg":"Employee data added successfully","status":"OK"}
        return jsonify(result)
    
@app.route('/update', methods = ['POST','GET'])
def update():
    data = request.get_json()
    emp_conn = Employees.query.get(data['empid'])
    if emp_conn:
        emp_conn.Name = data['name']
        emp_conn.Department = data['department']
        db.session.commit()
        result = {"msg":"Employee data updated successfully","status":"OK"}
        return jsonify(result)
    else:
        result = {"msg":"Employee data not available for updation","status":"error"}
        return jsonify(result)

@app.route('/delete', methods=['POST','GET'])
def delete():
    data = request.get_json()
    emp_id_check = Employees.query.get(data['empid'])
    if emp_id_check:
        db.session.delete(emp_id_check)
        db.session.commit()
        result = {"msg":"Employee data deleted successfully","status":"OK"}
        return jsonify(result)
    else:
        result = {"msg":"Employee data not available for deletion","status":"error"}
        return jsonify(result)

@app.route('/validemail', methods=['POST','GET'])
def validemail():
    data = request.get_json()
    emp_email_check = Employees.query.filter_by(Email=data['email']).first()
    if emp_email_check == data['email']:
        result = {"msg": "Email id is alredy available", "status": "error"}
        return jsonify(result)
    else:
        result = {"msg": "Email id is not available", "status": "ok"}
        return jsonify(result)

@app.route('/getdata', methods=['POST','GET'])
def getdata():
    data = request.get_json()
    emp_id = data['empid']
    emp_connection = Employees.query.get(emp_id)
    result = {"Name": emp_connection.Name,"Email":emp_connection.Email,"Department":emp_connection.Department}
    return jsonify(result)

