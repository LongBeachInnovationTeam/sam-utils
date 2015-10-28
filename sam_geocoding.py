#!/usr/bin/python
import logging
from pymongo import MongoClient
from geopy.geocoders import GoogleV3
from rate_limited_queue import RateLimitedQueue, RateLimit

LOG_FILENAME = 'sam-geocoding.log'
logging.basicConfig(filename = LOG_FILENAME, level = logging.INFO)

# Intialize mongo client and connect to database
client = MongoClient('localhost', 3001)
db = client['meteor']

# No more than ten addresses geocoded per second
rate_limit = RateLimit(duration = 1, max_per_interval = 10)

# Initialize GoogleV3
geolocator = GoogleV3()

def get_geocoded_list():
	# Create a list of all addresses
	addresses = get_unique_address_list()
	# Prepare a rate limited queue to execute the geocode function
	queue = RateLimitedQueue(
		addresses,
		processing_function = geolocator.geocode,
		rate_limits = [rate_limit]
	)
	# Grabs the geocoded locations, but doesn't process
	# more than ten per second
	geocoded_locations = queue.process()
	# Prepare our location document for DB insert
	addresses_list = list()
	for i in range(len(addresses)):
		address = addresses[i]
		if is_unique_address(address):
			location = geocoded_locations[i]
			if location is not None:
				logging.info("Found location info for '" + address + "'")
				addresses_list.append({
					"address": address,
					"longitude": location.longitude,
					"latitude": location.latitude
				})
	return addresses_list

def is_unique_address(address):
	for loc in db.locations.find():
		if loc['address'] is not address:
			return False
	return True

def get_unique_address_list():
	addresses = list()
	for c in db.contacts.find():
		if 'address' in c:
			a = c['address']
			if a not in addresses:
				addresses.append(a)
	return addresses

# Insert into db
addresses_list = get_geocoded_list()
if len(addresses_list) > 0:
	result = db.locations.insert_many(addresses_list)
	logging.info("Added " + str(len(result.inserted_ids)) + " new geolocations.")
