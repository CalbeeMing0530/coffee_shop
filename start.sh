#!/bin/bash
cd coffeen-web-ui
python manage.py migrate
screen -dmS coffeen-web-ui python manage.py runserver --insecure 0:8000

/bin/bash

