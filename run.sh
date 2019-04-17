#!/bin/bash

cd /code

pip install -r ${REQUIREMENTS_FILE:-requirements.txt}

if [[ "$1" == "bash" ]]
then
    bash
else
    uwsgi --virtualenv /env --chdir /code -w "${WSGI_MODULE:-wsgi:app}" --uwsgi-socket 0.0.0.0:5000
fi
