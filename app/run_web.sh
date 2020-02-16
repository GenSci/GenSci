#!/bin/bash
###################################################################
# run_web.sh
####################################################################
# This file is run whenever the web container is started.
###################################################################

# We wait 30 seconds to allow the database server to file up
sleep 2
# Creating migrations to catch any database changes we've made in our Django
#  applciation.
eval 'python3 manage.py makemigrations'

# Applying any changes we've made to our database.
eval 'python3 manage.py migrate'

# Now that our DB properly reflects our Django models, we can start our
# web application.
eval 'gunicorn gensci.wsgi --config=gunicorn.conf.py -w 4 -b :9000'
