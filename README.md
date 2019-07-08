# Product Importer App

A simple **Python-flask** app to import csv file which uses **celery + redis** to handle data load from csv to DB.
App is configured to with flask migrate and flask script, and uses postgresql DB. 

## Running the application.
* Create virtualenv and install the requirements thru 'pip install -r requirements.txt'
* psql db needs to be created with:
	* username: product_user
	* password: product_user
	* db_name: product_importer
* 'python app.py db init' followed by 'python app.py db upgrade'.
* Run the main application using - 'python app.py runserver'.
* Run the celery app in a seperate instance using - 'celery worker -A app.celery --loglevel=info'. 
