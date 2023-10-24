from flask import Flask, render_template
from db import Base, Patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# # Create a SQLite database (you can change this to your specific database)
DATABASE_URL = "mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/jason4c"
DATABASE_URL = "mysql+mysqlconnector://root:jasongooglecloud@34.27.164.47/jason4c2"
DATABASE_URL = "sqlite:///local.db"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
Base.metadata.bind = app

# Create a SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    # Retrieve data from the database
    patients = session.query(Patient).all()
    return render_template('index_tailwind.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)