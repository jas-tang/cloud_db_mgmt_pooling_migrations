from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI_AZURE'] = 'mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/jason4c'
app.config['SQLALCHEMY_DATABASE_URI_GCP'] = 'mysql+mysqlconnector://root:jasongooglecloud@34.27.164.47/jason4c2'

db_azure = SQLAlchemy(app, session_options={'autoflush': False})
db_gcp = SQLAlchemy(app, session_options={'autoflush': False})

class AzureModelPatients(db_azure.Model):
    id = db_azure.Column(db_azure.Integer, primary_key=True)
    first_name = db_azure.Column(db_azure.String(50), nullable=False)
    last_name = db_azure.Column(db_azure.String(50), nullable=False)
    date_of_birth = db_azure.Column(db_azure.Date, nullable=False)
    gender = db_azure.Column(db_azure.String(10), nullable=False)
    contact_number = db_azure.Column(db_azure.String(15))
    azure_is_active = db_azure.Column(db_azure.String(50), nullable=False)

class AzureModelMedicalRecord(db_azure.Model):
    id = db_azure.Column(db_azure.Integer, primary_key=True)
    patient_id = db_azure.Column(db_azure.Integer, db_azure.ForeignKey('patients.id'), nullable=False)
    diagnosis = db_azure.Column(db_azure.String(100), nullable=False)
    treatment = db_azure.Column(db_azure.String(200))
    admission_date = db_azure.Column(db_azure.Date, nullable=False)
    discharge_date = db_azure.Column(db_azure.Date)

class GCPModelPatients(db_gcp.Model):
    id = db_gcp.Column(db_gcp.Integer, primary_key=True)
    first_name = db_gcp.Column(db_gcp.String(50), nullable=False)
    last_name = db_gcp.Column(db_gcp.String(50), nullable=False)
    date_of_birth = db_gcp.Column(db_gcp.Date, nullable=False)
    gender = db_gcp.Column(db_gcp.String(10), nullable=False)
    contact_number = db_gcp.Column(db_gcp.String(15))
    is_active = db_gcp.Column(db_gcp.String(50), nullable=False)

class GCPModelMedicalRecord(db_gcp.Model):
    id = db_gcp.Column(db_gcp.Integer, primary_key=True)
    patient_id = db_gcp.Column(db_gcp.Integer, db_gcp.ForeignKey('patients.id'), nullable=False)
    diagnosis = db_gcp.Column(db_gcp.String(100), nullable=False)
    treatment = db_gcp.Column(db_gcp.String(200))
    admission_date = db_gcp.Column(db_gcp.Date, nullable=False)
    discharge_date = db_gcp.Column(db_gcp.Date)

@app.route('/patients/azure')
def azure_patients():
    azure_patients = AzureModelPatients.query.all()
    return render_template('patients.html', patients=azure_patients)

@app.route('/patients/gcp')
def gcp_patients():
    gcp_patients = GCPModelPatients.query.all()
    return render_template('patients.html', patients=gcp_patients)

@app.route('/medical_records/azure')
def azure_medical_records():
    azure_records = AzureModelMedicalRecord.query.all()
    return render_template('medical_records.html', records=azure_records)

@app.route('/medical_records/gcp')
def gcp_medical_records():
    gcp_records = GCPModelMedicalRecord.query.all()
    return render_template('medical_records.html', records=gcp_records)
    