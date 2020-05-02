from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
DATABASE_NAME = Configuration.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_NAME, echo=False, connect_args={'check_same_thread': False})

Session = scoped_session(sessionmaker(bind=engine))
session = Session()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
