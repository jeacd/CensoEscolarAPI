from flask_cors import CORS

from helpers.application import app

cors = CORS(resources={r"/*": {"origins": "*"}})
cors.init_app(app, resources={r"/*": {"origins": "*"}})