#!/usr/bin/python
import logging
import ConfigParser
from pymongo import MongoClient
from geopy.geocoders import GoogleV3
from rate_limited_queue import RateLimitedQueue, RateLimit
from address import AddressParser, Address

# Read options from our config file
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

LOG_FILENAME = config.get('logging', 'LOG_FILENAME')
logging.basicConfig(filename = LOG_FILENAME, level = logging.INFO)

# Intialize mongo client and connect to database
DB_NAME = config.get('database', 'DB_NAME')
HOSTNAME = config.get('database', 'HOSTNAME')
PORT = config.getint('database', 'PORT')
client = MongoClient(HOSTNAME, PORT)
db = client[DB_NAME]

# No more than ten addresses geocoded per second
rate_limit = RateLimit(duration = 1, max_per_interval = 10)

# Initialize GoogleV3
geolocator = GoogleV3()

# Initialize address parser
address_parser = AddressParser()

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
				logging.info("Found location info for '%s'", address)
				addresses_list.append({
					"address": address,
					"longitude": location.longitude,
					"latitude": location.latitude,
					"zipcode": address_parser.parse_address(location.address).zip
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
	logging.info("Added %d new geolocations.", len(result.inserted_ids))
else:
	logging.info("No new geolocations were found.")
