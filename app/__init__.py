from flask import render_template, Flask, url_for, session, redirect, request, abort, flash


DEBUG = True
SECRET_KEY = '12345678'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../store.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

pwdApp = Flask(__name__)
pwdApp.config.from_object(__name__)

from app import routes


