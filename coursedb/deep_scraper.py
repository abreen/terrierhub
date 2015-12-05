import sys
import os
import http.client
from urllib.parse import quote_plus
import json
import html5lib             # https://github.com/html5lib/html5lib-python
import re


#
# constants
#
HOST = 'www.bu.edu'
URL = '/phpbin/course-search/section/?t={}'
URL_OPENSEATS = '/phpbin/summer/rpc/openseats.php?{}'
ROW_KEYS = ['section', 'open_seats', 'instructor', 'type', 'location', 'meets_on',
            'dates', 'notes']
NS = {'html': 'http://www.w3.org/1999/xhtml'}


def error(msg):
    print(sys.argv[0] + ': error: ' + msg, file=sys.stderr)

def empty_result_row():
    return {
        '_id': None,
        'section': None,
        'open_seats': None,
        'instructor': None,
        'type': None,
        'notes': None,
        'meetings': []
    }

def sections_to_php_get(sections):
    return '&'.join(['sections[]=' + quote_plus(s) for s in sections])

def scrape(course_str):
    conn = http.client.HTTPConnection(HOST)

    conn.request('GET', URL.format(course_str))
    response = conn.getresponse()

    resp_str = response.read().decode('utf-8')
    doc = html5lib.parse(resp_str)

    # if the <h1> tag on this page is empty, the course string must be invalid
    # (this means BU can't match the course string to a course title)

    h1 = doc.find('.//html:h1', NS)

    if h1 is None or h1.text is None:
        error('invalid course string')
        return

    tables = doc.findall('.//html:table[@class="section-list"]', NS)

    if tables is None:
        # the course exists, but there are no sections scheduled
        return {}

    results = []

    for table in tables:
        rows = table.findall('.//html:tr', NS)
        rowspan = 1

        result_row = empty_result_row()

        for row in rows:
            ths = row.findall('./html:th', NS)
            if len(ths) > 0:
                # found a header row
                continue

            tds = row.findall('./html:td', NS)

            if rowspan == 1:
                # this row should not inherit data from a "parent" row

                if len(tds) == 0:
                    error('section list row has no data cells')
                    return

                section_id = row.attrib['data-section']
                if section_id is None:
                    error('section list row has no data-section attribute')
                    return

                result_row['_id'] = section_id

                rowspan = int(tds[0].attrib.get('rowspan', '1'))

                if len(tds) != len(ROW_KEYS):
                    error('unexpected number of data cells in section list row '
                          '(expected {}, found {})'.format(len(ROW_KEYS), len(tds)))
                    return

                # parse section
                result_row['section'] = tds[0].text.strip()

                # note: we will get the open seats numbers at the very end, since
                # they can only be obtained by another RPC call that this page
                # makes

                # parse instructor
                instructor_name = tds[2].text
                if instructor_name is not None:
                    result_row['instructor'] = instructor_name.strip()

                # parse section type (e.g., 'LEC' or 'LAB')
                result_row['type'] = tds[3].text.strip()

                # parse notes
                notes_td = tds[7]
                if notes_td.text is not None:
                    result_row['notes'] = notes_td.text.strip()

                meeting = {
                    'location': None,
                    'time': None,
                    'dates': None
                }

                meeting['location'] = tds[4].text.strip()
                meeting['time'] = tds[5].text.strip()
                meeting['dates'] = tds[6].text.strip()

                result_row['meetings'].append(meeting)

            else:
                # this row should inherit data from a previous "parent" row
                # (this row only specifies another item in the 'meetings' list)
                rowspan -= 1

                meeting = {
                    'location': None,
                    'time': None,
                    'dates': None
                }

                meeting['location'] = tds[1].text.strip()
                meeting['time'] = tds[2].text.strip()
                meeting['dates'] = tds[3].text.strip()

                result_row['meetings'].append(meeting)


            # just parsed either a regular row or a "parented" row
            if rowspan == 1:
                results.append(result_row)
                result_row = empty_result_row()


    # done getting most data; now make an RPC call for the open seats numbers
    section_ids = {}
    for result in results:
        section_ids[result['_id']] = result

    seats_url = URL_OPENSEATS.format(sections_to_php_get(section_ids.keys()))

    conn.request('GET', seats_url)
    response = conn.getresponse()
    resp_str = response.read().decode('utf-8')

    resp_json = json.loads(resp_str)
    seats = resp_json['results']

    if not seats:
        error('could not get open seats numbers')
        return results

    for section_id, open_seats in seats.items():
        if section_id not in section_ids:
            continue

        open_seats = int(open_seats)
        section_ids[section_id]['open_seats'] = open_seats

    return results
