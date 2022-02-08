import json
import requests

from resources.calc_distances import calc_haversine_dist_miles, calc_equirectangular_dist_miles
import pandas as pd
from numpy import nan

class GetUserDetails(object):

    def __init__(self, root_url, requested_city='London', find_users_in_range=True, requested_range=50, requested_lat_long=(51.506, -0.1272)):
        self._root_url = root_url

        self._requested_city = requested_city
        
        # set to (lat, long) of London as default
        self._requested_lat_long = requested_lat_long
        self._users = self.get_all_users()

        #If False, only return users who are listed as living in requested city, else also return users in the requested range
        self._find_users_in_range = find_users_in_range 
        
        if requested_range <0:
            requested_range*=-1

        self._requested_range = requested_range  # set to 50 miles by default

    def get_all_users(self):
        query_user_url = self._root_url + 'users'

        return pd.DataFrame((requests.get(query_user_url)).json())

    def get_total_num_of_users(self):
        number_of_users = self._users.shape[0]

        return number_of_users

    def get_user_keys(self):
        available_keys = self._users.columns.values.tolist()
        return available_keys

    def get_users_in_requested_city(self, input_city='London'):

        query_city_url = self._root_url + 'city/'+input_city+'/users'
        user_request = requests.get(query_city_url)
        users_in_city = pd.DataFrame(user_request.json())
        user_request.raise_for_status()

        return users_in_city

        
    def filter_users_by_distance(self, users,  requested_range=50, requested_lat_long=(51.506, -0.1272)):
        latitude = pd.to_numeric(users["latitude"])
        longitude = pd.to_numeric(users["longitude"])
        distance = calc_haversine_dist_miles(latitude, longitude, requested_lat_long)
        users['distance_from_city'] = distance

        users_within_range = users.loc[users['distance_from_city']
                                       <= requested_range]
        return users_within_range

    def get_all_users_near_city(self, requested_range=50, input_city='London', find_users_in_range=True , requested_lat_long=(51.506, -0.1272)):

        users_in_city = self.get_users_in_requested_city(input_city) # returns users listed as living in input_city
               
        if find_users_in_range == True: 
            users_in_range = self.filter_users_by_distance(self._users,
                                                       requested_range, requested_lat_long)
            all_users_in_city = (pd.concat(
                [users_in_range, users_in_city]).drop_duplicates(keep=False))
        else:
            all_users_in_city = (users_in_city).drop_duplicates(keep=False)
            all_users_in_city['distance_from_city']= nan

        all_users_in_city['distance_from_city']= all_users_in_city['distance_from_city'].fillna(value=0) 
        all_users_in_city = all_users_in_city.sort_values('id')

        return all_users_in_city


    def call_filter_users_for_test(self): 
        users_in_city = self.__filter_users_by_city_test()
        return users_in_city

    def __filter_users_by_city_test(self,  input_city='London'):

        number_of_users = int(self.get_total_num_of_users())
        number_relevant_users = 0
        for user_id in range(number_of_users):
            query_user_url = self._root_url + 'user/'+str(user_id+1)
            user = (requests.get(query_user_url)).json()
            if user['city'] == input_city:
                number_relevant_users += 1
        return number_relevant_users

   
