from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456789@localhost:5434/censoescolar"

api = Api(app)