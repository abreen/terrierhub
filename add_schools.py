import sys
from coursedb.models import School

if len(sys.argv) != 2:
    print('usage: {} schools_tsv_path'.format(sys.argv[0]))
    sys.exit(1)

path = sys.argv[1]

with open(path, 'r') as f:
    for dept in f:
        symbol, name = dept.split('\t')

        symbol = symbol.strip()
        name = name.strip()

        s = School(symbol=symbol, name=name)
        s.save()

        print('added school ' + name + ' (' + symbol + ')')
