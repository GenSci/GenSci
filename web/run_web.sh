#!/bin/bash
###############################################################################
# run_web.sh
###############################################################################
# This file is run whenever the web container is started.
###############################################################################

# Creating migrations to catch any database changes we've made in our Django
#  applciation.
eval 'python3 manage.py makemigrations'

# Applying any changes we've made to our database.
eval 'python3 manage.py migrate'

# Now that our DB properly reflects our Django models, we can start our
# web application.
eval 'gunicorn GenSci.wsgi -w 4 -b :9000'
