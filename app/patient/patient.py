from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
import pika

app = Flask(__name__)
#Access the order table in myphpadmin database. (After importing patient.sql files)
#I AM USIG PORT 3308 AND ESD_PATIENT DATABASE!
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/esd_patient'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    salutation  = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)   

    def json(self):
        dto = {
            'patient_id': self.patient_id, 
            'name': self.name,
            'gender' : self.gender ,
            'dob' : self.dob ,
            'phone' : self.phone ,
            'salutation' : self.salutation ,
            'username' : self.username ,
            'password' : self.password 
        }
        return dto  
#Note that post does not have anything in the url. Its all in the body of the request
#@app.route("/login-process/<string:username>&<string:password>", methods=['POST'])
@app.route("/login-process", methods=['POST'])
def login():
    data = request.get_json()
    patient = Patient.query.filter_by(username=data["username"]).filter_by(password=data["password"]).first()
    if patient:
        return jsonify(patient.json())
    return jsonify({'message': 'Wrong username/password! '}), 404   

@app.route("/register-process", methods=['POST'])
def register():
    data = request.get_json()
    #Checks if there exists another patient with the same username
    if (Patient.query.filter_by(username=data["username"]).first()):
        return jsonify({"message": "A patient with username '{}' already exists.".format(data['username'])}), 400
    #I changed everything to string in sql database as there will be error if you submit a string to a column defined as integer
    data = request.get_json()
    #We use **data to retrieve all the info in the data array, which includes username, password, salutation, name, dob etc
    patient = Patient(**data)
    try:
        db.session.add(patient)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the patient."}), 500
 
    return jsonify(patient.json()), 201

@app.route("/update-profile-process", methods=['POST'])
#Retrieves a specific patient details
def getPatient():
    data = request.get_json()
    patient = Patient.query.filter_by(username=data["username"]).first()
    if patient:
        return jsonify(patient.json())
    return jsonify({'message': 'Wrong username/password! '}), 404   

@app.route("/update-profile-update", methods=['POST'])
#Updates a specific patient details
def updatePatient():
    #I changed everything to string in sql database as there will be error if you submit a string to a column defined as integer
    data = request.get_json()
    #Checks if the provided password is correct
    patient = Patient.query.filter_by(username=data["username"]).first()
    patientdata = patient.json()
    if (data["checkpassword"] != patientdata["password"]):
        return jsonify({"message": "The provided password is wrong."}), 400
    #Checkpassword is only used to check whether the user provided the correct oldpassword. After checking we need to delete it
    #as we do not want it in sql database. The newpassword is already stored in password
    #del data["checkpassword"]
    #We use **data to retrieve all the info in the data array, which includes username, password, salutation, name, dob etc
    #patient = Patient(**data)
    try:
        setattr(patient, 'name', data["name"])
        setattr(patient, 'gender', data["gender"])
        setattr(patient, 'dob', data["dob"])
        setattr(patient, 'phone', data["phone"])
        setattr(patient, 'salutation', data["salutation"])
        setattr(patient, 'password', data["password"])
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating details of the patient."}), 500
 
    return jsonify(patient.json()), 201

@app.route("/order_db") #Going to /order_db will redirect you to this order_db.py file
def get_all():
    return {'orders': [order.json() for order in Order.query.all()]}
#THis is for flask ap
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)