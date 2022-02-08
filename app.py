import json
import requests
from flask import Flask
from flask_restx import Api, Resource

flask_app = Flask(__name__)
flask_api = Api(flask_app, version='0.1', title='User Distance API',
                description='API to call the bpdts-test-app API and returns users listed in a city, within a given distance from a city e.g. within 50 miles from London by default')

api_namespace = flask_api.namespace("user_distances")


import resources.routes






