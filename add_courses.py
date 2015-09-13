import sys
import django
from coursedb.models import School, Department, Course

if len(sys.argv) != 2:
    print('usage: {} courses_tsv_path'.format(sys.argv[0]))
    sys.exit(1)

path = sys.argv[1]

django.setup()

with open(path, 'r') as f:
    for course in f:
        school_sym, dept_sym, num, note, desc = course.split('\t')

        school_sym = school_sym.strip()
        dept_sym = dept_sym.strip()
        note = note.strip()
        desc = desc.strip()

        try:
            s = School.objects.get(symbol=school_sym)
        except:
            print('could not find school', school_sym)
            continue

        try:
            d = Department.objects.get(school=s, symbol=dept_sym)
        except:
            print('could not find department', dept_sym, 'for school', s)
            continue

        c = Course(department=d, number=int(num), description=desc, note=note)
        c.save()

        print('added', str(c))
