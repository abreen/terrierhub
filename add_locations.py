import sys
from coursedb.models import Location

if len(sys.argv) != 2:
    print('usage: {} locations_tsv_path'.format(sys.argv[0]))
    sys.exit(1)

path = sys.argv[1]

with open(path, 'r') as f:
    for loc in f:
        symbol, address, lat, lng = loc.split('\t')

        symbol = symbol.strip()
        address = address.strip()
        lat = lat.strip()
        lng = lng.strip()

        l = Location(
                symbol=symbol,
                address=address,
                latitude=lat,
                longitude=lng
        )
        l.save()

        print('added location ' + symbol)
