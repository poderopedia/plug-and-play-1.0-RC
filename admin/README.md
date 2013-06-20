SetUP PowerMapa
======

##Contents:
* Requirements
* Initial Configuration


##Requirements
* github
* Python 2.7 installed
* web2py Framework installed and running.
* A Database (MySql or PostgreSQL) installed
* Additional Python libs urllib2, request, libxml2, [rdflib](https://github.com/RDFLib), [rdfAlchemy](https://rdfalchemy.readthedocs.org/en/latest/)
* Web Server (for Production environments) Nginx / Apache (script for config both web-servers are provided in the Script directory). Example `scripts> . setup-web2py-nginx-uwsgi-on-centos.sh`

##Optional Requirements for Production
* Memcached (if you plan use a caching server)


## Install:
You must clone the github repo, under the applications directory in the web2py installation:

 `cd path_to web2py/applications`

 `git clone https://github.com/poderopedia/powermapa.git`


##Initial Configuration
There are 3 main config files in the models directory:

* 0.py - contains all mayor settings (database_uri, meta-content, application name, mail-server settings, etc.)
* 0_memcached - the connection config for the memcached server.
* document_cloud.py - contains the credentials to autentificate in DocumentCloud.org.

You must write your settings in these 3 files.



##Testing the Installation
In localhost, you must check http://localhost:8000/powermapa
At this point you have created all data models in your database, you only need Pre-poluate some data. Before this you need change the migrate attribute in the file 0.py from True to False, for example: `settings.migrate=False`


##Pre - Populate:
Before running the full application you needs some initial data (pre-polulate the database and identifying the super-Adminsitrator. 
For pre-populate the data you must access to the following url in localhost: `http://localhost:8000/powermapa/install`




That's it.












