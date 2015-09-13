#!/bin/bash

# use Django tools to set up empty database
python3 manage.py migrate

# add all schools
python3 add_schools.py rawdata/schools.tsv

# add departments
python3 add_depts.py CAS rawdata/cas/depts.tsv
python3 add_depts.py CFA rawdata/cfa/depts.tsv
