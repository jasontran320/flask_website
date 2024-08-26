from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS#This is to fix the cross reference policy thing that shows up sometimes

app = Flask(__name__)
CORS(app)#Avoid the cross policy origin issue

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///friends.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)