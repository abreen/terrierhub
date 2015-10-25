#!/bin/bash

if [[ -e db.sqlite3 ]]; then
    echo error: database already present
    exit 1
fi

export DJANGO_SETTINGS_MODULE=courses.settings

# use Django tools to set up empty database
python3 manage.py migrate || exit 2

# add all schools
python3 add_schools.py rawdata/schools.tsv || exit 3

# add all locations
python3 add_locations.py rawdata/locations.tsv || exit 4

# add departments
python3 add_depts.py CAS rawdata/cas/depts.tsv || exit 5
python3 add_depts.py CFA rawdata/cfa/depts.tsv || exit 5

# add courses
python3 add_courses.py rawdata/cas/courses.tsv || exit 6
python3 add_courses.py rawdata/cfa/courses.tsv || exit 6
