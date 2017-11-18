import json
import re
import pycountry
from geopy.geocoders import Nominatim
from pprint import pprint
import geopy
from flask_pymongo import pymongo

with open('providers.geojson', encoding="utf8") as data_file:    
    data = json.load(data_file)

languages = set()
for language in pycountry.languages:
    languages.add(language.name)

client = pymongo.MongoClient()
db = client.interceptDB
organization_collection = db.organizations
for ngo in data['accountsWithGeo']['features']:
    # Do stuff here
    info = ngo['properties']
    geolocator = Nominatim()
    location = geolocator.geocode(info.get('address', '') + ', '
                                    + info.get('city', '') + ', '
                                    + info.get('state', ''))
    if 'phone2' in info:
        phone_numbers = [info.get('phone', ''), info.get('phone2', '')]
    elif 'phone' in info:
        phone_numbers = [info.get('phone', '')]
    else:
        phone_numbers = []
    services = info.get('servicesDetailNotes', {})
    for service in info.get('servicesDetail', []):
        if service not in services:
            services[service] = ''
    
    messy_languages = set(re.split(' |;|,|\*|\n', info.get('languages', '')))
    ngo_languages = languages.intersection(messy_languages)
    ngo_languages.add('English')
    ngo_detail = {
        'name': info.get('name', ''),
        'mission_statement': info.get('missionStatement', ''),
        'contact_info': {
            'website': info.get('website', ''),
            'phone_numbers': phone_numbers,
            'hotline': {
                'number': info.get('hotline', ''),
                'notes': info.get('hotlineNotes', '')
            },
            'email': info.get('email', ''),
            'location': {
                'address': info.get('address', ''),
                'city': info.get('city', ''),
                'state': info.get('state', ''),
                'country': info.get('country', 'United States')
                }
            },
        'coordinates': {
            'latitude': location.latitude if location is not None else ngo['geometry']['coordinates'][0],
            'longitude': location.longitude if location is not None else ngo['geometry']['coordinates'][1]
            },
        'services': services,
        'service_area': info.get('serviceArea', ''),
        'populations': info.get('populationsDetail', []),
        'languages': list(ngo_languages)
        }
    organization_collection.insert_one(ngo_detail)

