#!/bin/bash

if [[ -e db.sqlite3 ]]; then
    echo error: database already present
    exit 1
fi

# use Django tools to set up empty database
python3 manage.py migrate || exit 2

# add all schools
python3 add_schools.py rawdata/schools.tsv || exit 3

# add departments
python3 add_depts.py CAS rawdata/cas/depts.tsv || exit 4
python3 add_depts.py CFA rawdata/cfa/depts.tsv || exit 4

# add courses
#python3 add_courses.py rawdata/cas/courses.tsv || exit 5
python3 add_courses.py rawdata/cfa/courses.tsv || exit 5
