from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import tasks

app = Flask(__name__)
# config to log SQL output
# SQLALCHEMY_ECHO=True
app.config.update(
    SQLALCHEMY_DATABASE_URI="postgresql://localhost/travel_notifications",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

tasks.run_backgrounder()
