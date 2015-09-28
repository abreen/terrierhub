import sys
from coursedb.models import School, Department

if len(sys.argv) != 3:
    print('usage: {} school_symbol departments_tsv_path'.format(sys.argv[0]))
    sys.exit(1)

school_symbol = sys.argv[1]
path = sys.argv[2]

try:
    school = School.objects.get(symbol=school_symbol)
except:
    print('could not find school ' + school_symbol + ' in database')
    print('did you add the schools first?')
    sys.exit(2)

with open(path, 'r') as f:
    for dept in f:
        symbol, name = dept.split('\t')

        symbol = symbol.strip()
        name = name.strip()

        d = Department(school=school, symbol=symbol, name=name)
        d.save()

        print('added ' + name + ' (' + symbol + ') to school ' + str(school))
