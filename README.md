# cloud_db_mgmt_pooling_migrations
This is a repository for Assignment 4C in HHA504. 

# Connection Pooling Setup 

Start by starting an Azure Database for MySQL servers. 
![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/azure%20setup.png)

and a GCP server
![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/gcp%20server.JPG)

# Database Schema and Data

## Azure
We then ran this code to create two tables (Patients and Medical Records) within the database: 
```
## Part 1 - Define SQLAlchemy models for patients and their medical records:
### this file below could always be called db_schema.py or something similar

from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_number = Column(String(15))
    azure_is_active = Column(String(50), nullable =False)

    records = relationship('MedicalRecord', back_populates='patient')

class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    diagnosis = Column(String(100), nullable=False)
    treatment = Column(String(200))
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date)

    patient = relationship('Patient', back_populates='records')


### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine("mysql+pymysql://######:########*@jason-azure.mysql.database.azure.com/jason4c",
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
                         )

## Test connection

inspector = inspect(engine)
inspector.get_table_names()


### Part 3 - create the tables using sqlalchemy models, with no raw SQL required:

Base.metadata.create_all(engine)
```

Then create the engine so that sqlalchemy can connect to it
```
engine = create_engine("mysql+pymysql://hants:sbu-admin-2023@hants-migrations-test.mysql.database.azure.com/hants",
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
```

We can test the connection with:
```
inspector = inspect(engine)
inspector.get_table_names()
```

However, I ran across an error while running the code that created Python Classes. I was only able to load the Patient Class as a table, not not Medical Records. 

![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/error.JPG)
![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/error2.JPG)

I was able to solve the issue by running the code in its entirely instead of one by one. 

![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/error2solution.JPG)

## GCP
Similarly, we ran similar code in GCP. 

```
## Part 1 - Define SQLAlchemy models for patients and their medical records:
### this file below could always be called db_schema.py or something similar

from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_number = Column(String(15))

    records = relationship('MedicalRecord', back_populates='patient')

class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    diagnosis = Column(String(100), nullable=False)
    treatment = Column(String(200))
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date)

    patient = relationship('Patient', back_populates='records')


### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine("mysql+mysqlconnector://hants-test:yourpassword@34.139.18.69/hants")

## Test connection

inspector = inspect(engine)
inspector.get_table_names()


### Part 3 - create the tables using sqlalchemy models, with no raw SQL required:

Base.metadata.create_all(engine)
```

This created two tables again, one for Patients, one for medical records.

# Database Migrations with Alembic

For both instances of GCP and Azure, we followed these steps. 
```
1. alembic init migrations
` alembic init migrations `

2. edit alembic.ini to point to your database
` sqlalchemy.url = mysql+mysqlconnector://username:password@host/database_name `

3. edit env.py to point to your models
`from db_schema import Base`
`target_metadata = Base.metadata `

4. create a migration
` alembic revision --autogenerate -m "create tables" `

5. run the migration
` alembic upgrade head `
```
For both instances, it created a migrations folder with an Alembic.ini and migration.sql. It also created a versions folder for any new updates. 

# Using MySQL Workbench to Generate ERD

I was able to connect to both servers on mySQL workbench and generate their ERD's. 
![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/azure%20erd.JPG)
![](https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/gcp%20erd.JPG)

# SQLAlchemy and Flask Integration 

Creating this flask integration with SQLAlchemy while connecting to the SQL servers on Azure and GCP was a little challenging. 

This was my app.py code: 
```
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_BINDS'] = {
    'azure': 'mysql+pymysql://###########
    'gcp': 'mysql+mysqlconnector://#############

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
```
It was important to create a class for each table on each database. This was so you can access all the information on each table separately on one singular flask application. 

This was the base.html. 
```
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment 4C</title>
    
    <!-- Tailwind CSS via CDN -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>

<body class="bg-gray-200">

    <header class="bg-red-600 text-white p-4">
        <h1 class="text-4xl">Assignment 4C</h1>
        <nav>
            <ul class="flex space-x-4">
                <li><a href="/" class="hover:underline">Home</a></li>
                <li><a href="{{ url_for('azure_patients') }}" class="hover:underline">Azure (Patients Table)</a></li>
                <li><a href="{{ url_for('azure_medical_records') }}" class="hover:underline">Azure (Medical Records Table)</a></li>
                <li><a href="{{ url_for('gcp_patients') }}" class="hover:underline">GCP (Patients Table)</a></li>
                <li><a href="{{ url_for('gcp_medical_records') }}" class="hover:underline">GCP (Medical Records Table)</a></li>
            </ul>
        </nav>
    </header>

    <main class="p-4">
        <h2 class="text-2xl"></h2>
        <p>Click on the above links to access different tables for each database.</p>
        </p>Patients and Medical Records tables or located in Microsoft Azure and Google Cloud Services. <p>
    
    </main>

    <main class="p-4">

        {% block content %}{% endblock %}

    </main>

    <footer class="bg-red-600 text-white p-4 mt-6">
        <p>Check <a href="https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations">Github</a> for more information</p>
    </footer>

    <style>
        a:link {
          color: green;
          background-color: transparent;
          text-decoration: none;
        }
        a:visited {
          color: pink;
          background-color: transparent;
          text-decoration: none;
        }
        a:hover {
          color: red;
          background-color: transparent;
          text-decoration: underline;
        }
        a:active {
          color: yellow;
          background-color: transparent;
          text-decoration: underline;
        }
        </style>

</body>

</html>
```
The rest of the html files are found within my github. 

https://github.com/jas-tang/cloud_db_mgmt_pooling_migrations/blob/main/media/gcpazure.mov
