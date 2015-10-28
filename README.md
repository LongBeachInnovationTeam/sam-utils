# sam-geolocation-import

## About

A python script to populate contact geolocation information for the [SAM CRM web application](https://github.com/LongBeachInnovationTeam/sam-contacts).

For each new unique address found for a contact, the address, latitude, and longitude are added to the **locations** table of the **sam-contacts** meteor/mongo database.

##File Structure

This repository contains the following files:

    * sam_geocoding.py	- script to insert found geolocation info into the locations table
    * requirements.txt	- list of required dependencies to install through pip
    * sam_geocoding.sh 	- shell script to execute sam_geocoding.py in a scheduled crontab

## Dependencies

The following python modules/libraries are used by this project and installed through pip via **requirements.txt**:

- [`pymongo`](https://pypi.python.org/pypi/pymongo)
- [`geopy`](https://pypi.python.org/pypi/geopy)
- [`rate_limited_queue`](https://pypi.python.org/pypi/rate_limited_queue/0.0.6)
    
##Deployment

*These instructions have only been tested on a fresh Ubuntu 14.04 instance. YMMV.*

### Install and Configure virtualenv
On the command line, create a virtualenv called **sam-data** for this project:

1. Install pip `sudo apt-get install python-pip`
2. Install virtualenv `sudo pip install virtualenv`
3. Create a dir to store this and future virtualenvs `mkdir ~/.virtualenvs`
4. Install virtualenvwrapper `sudo pip install virtualenvwrapper`
5. Set WORKON_HOME to your virtualenv dir `export WORKON_HOME=~/.virtualenvs`
6. Add this line to the end of ~/.bashrc so that the virtualenvwrapper commands are loaded `. /usr/local/bin/virtualenvwrapper.sh` 
7. Reload .bashrc with the command `. .bashrc`
8. Create a new virtualenv `mkvirtualenv sam-data`

### Install Dependencies
Install required dependencies on the **sam-data** virtualenv with pip:

	cd sam-geolocation-import
	workon sam-data
	pip install -r requirements.txt