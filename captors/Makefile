#######################
# Cmd projet Django   #
#######################

# Local development management
clean:
	find -L curling_tournament/ -name "*~" -exec rm -fr {} \;
	find -L curling_tournament/ -name "*.pyc" -exec rm -fr {} \;
	find -L curling_tournament/ -name ".DS_Store" -exec rm -fr {} \;
	find -L curling_tournament/ -name "Thumbs.db" -exec rm -fr {} \;
	find -L curling_tournament/ -name "Thumbs.db:encryptable" -exec rm -fr {} \;

runserver:
	python manage.py runserver 0.0.0.0:8000

gunicorn:
	gunicorn captor_mesh.wsgi:application -b 0.0.0.0:8000 -w 3

cp_settings:
	-diff -u curling_tournament/settings.py ./settings.py.example 
	cp curling_tournament/settings.py ./settings.py.example

dumpdata:
	python manage.py dumpdata --natural --exclude=admin --exclude=south --exclude=contenttypes --exclude=auth --exclude=sessions --format yaml --indent=4 > curling_tournament_data.yaml

mail:
	python -m smtpd -n -c DebuggingServer localhost:1025

syncdb:
	# Flush the database
	python manage.py flushwebsite
        # Create empty databases
	python manage.py syncdb --noinput --migrate
        # Load the fixtures
	#python manage.py createwebsite
	#python manage.py loaddata curling_tournament_data.yaml
	python manage.py createsuperuser

# Testing suite
# test:
# 	python manage.py test

# Deployment management
collectstatic:
	python manage.py collectstatic --noinput

# Virtual Env Management
virtualenv:
	virtualenv --no-site-packages --distribute apps

upgrade: requirements.txt
	pip install -r requirements.txt

requirements:
	pip freeze > requirements.txt