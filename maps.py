import json
import math
import asyncio
import itertools
import traceback
import webbrowser
from pprint import pprint
import os
import yaml
import aiohttp
import folium

import streetview
def distance(p1, p2):
    """ Haversine formula: returns distance for latitude and longitude coordinates"""
    R = 6373
    lat1 = math.radians(p1[0])
    lat2 = math.radians(p2[0])
    lon1 = math.radians(p1[1])
    lon2 = math.radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R*c
global panoids
with open(f'panoids.json','r') as f:
    panoids = json.load(f)

def main():
    # Init variables
    file = 'maps.html'
    zoom_start = 12
    ## Read configuration from yaml file
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        center = config['center']
        radius = config['radius']
        resolution = config['resolution']
    top_left = (center[0]-radius/70, center[1]+radius/70)
    bottom_right = (center[0]+radius/70, center[1]-radius/70)

    lat_diff = top_left[0] - bottom_right[0]
    lon_diff = top_left[1] - bottom_right[1]

    # Create map
    M = folium.Map(location=center, tiles='OpenStreetMap', zoom_start=zoom_start)

    # Show lat/lon popups
    M.add_child(folium.LatLngPopup())

    # Mark Area
    folium.Circle(location=center, radius=radius*1000, color='#FF000099', fill='True').add_to(M)

    # Get testing points
    test_points = list(itertools.product(range(resolution+1), range(resolution+1)))
    test_points = [(bottom_right[0] + x*lat_diff/resolution, bottom_right[1] + y*lon_diff/resolution) for (x,y) in test_points]
    test_points = [p for p in test_points if distance(p, center) <= radius]
    
    # Add points streetview locations
    for pan in panoids:
        folium.CircleMarker([pan['lat'], pan['lon']], popup=pan['panoid'], radius=1, color='blue', fill=True).add_to(M)

    ## Save map and open it
    M.save(file)
    webbrowser.open(file)

if __name__ == "__main__":
    main()