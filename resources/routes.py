import requests
import json

from flask_restx import Resource, abort, reqparse, inputs

from resources.get_user_details import GetUserDetails
from app import flask_api, api_namespace

from werkzeug.exceptions import BadRequest, InternalServerError

DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'

parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('city', type=str,default='London', help='The city used to query the bpdts-test-app API for users listed as living in that city. \n e.g., default value of London will return all users who list themselves as living in London. ', location='args')
parser.add_argument('return_users', type=inputs.boolean, default=False, help='Optionally, also return users who meet criteria as part of the query',location='args')
parser.add_argument('find_users_in_range', type=inputs.boolean, default=True, help='When set to false, only users who are listed as living in a city are counted and distance, latitude and longitude are ignored. \n Set to true to also obtain users in range of given latitude and longitude.',location='args')
parser.add_argument('distance', type=float, default=50.0, help='Distance from a given location to search for users, set find_users_in_range to true to use this parameter.', location='args')
parser.add_argument('latitude', type=float, default=51.506 ,help='Latitude of location used for distance search. Set find_users_in_range to true to use this parameter. \n Default value is the latitude of London.', location='args')
parser.add_argument('longitude', type=float, default=-0.1272 , help='Longitude of location used for distance search. Set find_users_in_range to true to use this parameter. \n Default value is the longitude of London.', location='args')

@api_namespace.route('/information')
class ApiInfo(Resource):
    def get(self):
        return {'api_overview': 'todo'}

@api_namespace.doc(responses={ 200: 'OK', 400: 'Bad Request', 500: 'Internal Server Error' })
@api_namespace.route('/get_number_of_users_in_range/', doc={"description": 'By default, this request (/user_distances/get_number_of_users_in_range/) returns the number of users who are either listed as living in London, or whose current coordinates are within 50 miles of London. \n \n This request can also be modified to find users listed as living in any city, but the longitude and latitude must be updated to match this city to give a valid result for users in range. \n  Otherwise, set   find_users_in_range   to false to return users listed as living in the requested city. '})

class GetUsersGeneric(Resource):
    @api_namespace.expect(parser)
    def get(self):

        try: 
            args = parser.parse_args()

            requested_lat_long = (args['latitude'], args['longitude'])
            GUD = GetUserDetails(DATA_ROOT_URL)
             
            users_near_city = (GUD.get_all_users_near_city(args['distance'], args['city'], args['find_users_in_range'], requested_lat_long)).to_dict(orient='records')

            if args['return_users']==False:
                return {'number_of_users': len(users_near_city)}
            else: 
                return {'number_of_users': len(users_near_city), 'users' : users_near_city}

        except BadRequest as e:
            api_namespace.abort(400, str(e), status = "Bad Request", statusCode = "400")
        except Exception as e:
            api_namespace.abort(500, str(e), status = "Internal Server Error", statusCode = "500")


@api_namespace.doc(responses={ 200: 'OK', 400: 'Bad Request', 500: 'Internal Server Error' })
@api_namespace.route('/get_total_number_of_users',doc={"description": "Returns the total number of users that are available in the bpdts-test-app "})

class ApiInfo(Resource):
    def get(self):
        try:               
            GUD = GetUserDetails(DATA_ROOT_URL)
            total_number_of_users = GUD.get_total_num_of_users()
            return {'total_number_of_users': total_number_of_users}
        except BadRequest as e:
            api_namespace.abort(400, str(e), status = "Bad Request", statusCode = "400")
        except Exception as e:
            api_namespace.abort(500, str(e), status = "Internal Server Error", statusCode = "500")
