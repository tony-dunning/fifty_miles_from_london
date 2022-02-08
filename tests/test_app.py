
import pytest
import requests
import json
import time

from resources.get_user_details import GetUserDetails
from app import api_namespace
from werkzeug.exceptions import BadRequest, InternalServerError

name_space = api_namespace.name
url = 'http://127.0.0.1:5000/'+name_space 

DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'

def test_response():
    response = requests.get(url + '/information')
    assert response.status_code == 200


def test_app_output():
    response = requests.get(url + '/information')
    expected_output = {'api_overview': 'todo'}
    assert expected_output == response.json()


def test_total_number_of_users():
    expected_total_users = 1000
    response = requests.get(url + '/get_total_number_of_users')
    response_as_dict = response.json()
    num_of_users_returned = response_as_dict['total_number_of_users']
    assert int(num_of_users_returned) == expected_total_users

def test_users_in_50miles():
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city=London&return_users=false&find_users_in_range=true&distance=50&latitude=51.506&longitude=-0.1272')).json()
    response_london_specific = (requests.get(url + '/get_number_of_users_in_range')).json()

    assert response_general['number_of_users'] == response_london_specific['number_of_users']

def test_junk_input_response():
    response_general = (requests.get(url + '/get_number_of_users_in_range/?junk')).json()
    response_london_specific = (requests.get(url + '/get_number_of_users_in_range')).json()

    assert response_general['number_of_users'] == response_london_specific['number_of_users']

def test_check_error_handling():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Sheffield'
    test_latitude = '1.2345'
    test_longitude = '1.2345'
    test_find_users_in_range = 'true'
    test_return_users = 'true'
    

    response_general = requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range+'distance=50&latitude='+test_latitude+'&longitude='+test_longitude)   

    assert response_general.status_code == 400

def test_returned_keys():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Sheffield'
    test_find_users_in_range = 'false'
    test_return_users = 'false'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    
    expected_keys = ['number_of_users']
    assert expected_keys == list(response_general.keys())


def test_returned_keys_users():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Sheffield'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    
    expected_keys = ['number_of_users', 'users' ]
    assert expected_keys == list(response_general.keys())

def test_users_for_returned_city():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Sheffield'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    response_from_gud = GUD.get_users_in_requested_city(test_city)

    for i, v in enumerate (response_from_gud['id'].values):
        if response_general['users'][i]['id'] != v :
            assert False
    assert True


def test_returned_cities():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Sheffield'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()

    for user in response_general['users']:
        test_user_response = (requests.get(DATA_ROOT_URL + '/user/'+ str(user['id']))).json()

        if test_user_response['city'] != test_city :
            assert False
            return
    assert True
 


 

def test_compare_calc_methods():
    GUD = GetUserDetails(DATA_ROOT_URL)
    tic = time.perf_counter()
    user_distances_haversine = GUD.filter_users_by_distance(GUD._users)
    toc = time.perf_counter()
    tictotoc = toc - tic


    print(f"\nHaversine calculation ran in {tictotoc:0.5f} seconds\n")

