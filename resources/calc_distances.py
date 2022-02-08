import numpy as np

lat_long_london = (51.506, -0.1272)

def calc_haversine_dist_miles(lat_1, long_1, lat_long_2=lat_long_london, earth_radius=3956):

    assert len(lat_1) == len(long_1)
    vector_ones = np.ones(len(lat_1))
    lat_2 = vector_ones * lat_long_2[0]
    long_2 = vector_ones * lat_long_2[1]

    latitude_1, longitude_1, latitude_2, longitude_2 = np.radians(
        [lat_1, long_1, lat_2, long_2])

    delta_long = longitude_1 - longitude_2
    delta_lat = latitude_1 - latitude_2

    a = (np.sin(delta_lat/2))**2 + np.cos(latitude_1) * \
        np.cos(latitude_2) * (np.sin(delta_long/2))**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = earth_radius * c

    return distance
