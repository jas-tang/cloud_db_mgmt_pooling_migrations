from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_BINDS'] = {
    'azure': 'mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/jason4c',
    'gcp': 'mysql+mysqlconnector://root:jasongooglecloud@34.27.164.47/jason4c2',
} 

db = SQLAlchemy(app, session_options={'autoflush': False})

class AzureModelPatients(db.Model):
    __bind_key__ = 'azure'
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(15))

class AzureModelMedicalRecord(db.Model):
    __bind_key__ = 'azure'
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(200))
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)

class GCPModelPatients(db.Model):
    __bind_key__ = 'gcp'
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(15))


class GCPModelMedicalRecord(db.Model):
    __bind_key__ = 'gcp'
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(200))
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/patients/azure')
def azure_patients():
    azure_patients = AzureModelPatients.query.all()
    return render_template('patients.html', patients=azure_patients)   

@app.route('/medical_records/azure')
def azure_medical_records():
    azure_records = AzureModelMedicalRecord.query.all()
    return render_template('medical_records.html', records=azure_records)

@app.route('/patients/gcp')
def gcp_patients():
    gcp_patients = GCPModelPatients.query.all()
    return render_template('gcp_patients.html', patients=gcp_patients)

@app.route('/medical_records/gcp')
def gcp_medical_records():
    gcp_records = GCPModelMedicalRecord.query.all()
    return render_template('gcp_medical_records.html', records=gcp_records)


if __name__ == '__main__':
    app.run(debug=True)