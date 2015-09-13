# TODO the MET has a completely different page format ('/academics/met/courses/')
# TODO lots of the school abbrev.s redirect to COM?
# TODO the 'smg' school lists courses starting with 'GSM'?

import sys
import os
import http.client
import html5lib             # https://github.com/html5lib/html5lib-python
import re
import time


PATTERN = r'(CAS|CFA|CGS|COM|ENG|EOP|FRA|GMS|GRS|GSM|LAW|MED|MET|OTP|PDP|SAR|SDM|SED|SHA|SMG|SPH|SSW|STH|UNI|XAS|XRG)\s+([A-Z]+)\s+(\d+)'
SCHOOLS = ['cas', 'cfa', 'cgs', 'com', 'eng', 'gms', 'grs', 'law', 'sar', 'sdm',
           'sed', 'sha', 'smg', 'sph', 'ssw', 'sth']
COURSES_HOST = 'www.bu.edu'
COURSES_URL = '/academics/{}/courses/'
DATA_DIR = 'rawdata'

pat = re.compile(PATTERN)
ns = {'html': 'http://www.w3.org/1999/xhtml'}

conn = http.client.HTTPConnection(COURSES_HOST)

for school in ['cfa']:
    print('scraping courses for school', school)

    school_dir_path = DATA_DIR + os.sep + school

    if not os.path.isdir(school_dir_path):
        os.makedirs(school_dir_path)

    f = open(school_dir_path + os.sep + 'courses.tsv', 'w')

    # request the first page
    conn.request('GET', COURSES_URL.format(school))
    response = conn.getresponse()

    # process the first page
    resp_str = response.read().decode('utf-8')
    doc = html5lib.parse(resp_str)

    # get page limit (the <a> element) & set up loop
    lim = doc.find('.//html:div[@class="pagination"]/html:span[last()]/html:a', ns)
    if lim is None:
        print('error: cannot find page limit for', school)
        continue

    lim_num = int(lim.text)

    print('scraping', lim_num, 'pages...')

    url_prefix = COURSES_URL.format(school)

    for page in range(1, lim_num + 1):
        print('scraping page', page)

        url = url_prefix + str(page) + '/'

        conn.request('GET', url)
        response = conn.getresponse()

        resp_str = response.read().decode('utf-8')

        doc = html5lib.parse(resp_str)

        ul = doc.find('.//html:ul[@class="course-feed"]', ns)

        if ul is None:
            print('invalid HTML in response for', school, page)
            continue

        for li in ul.findall('html:li', ns):
            strong = li.find('html:a/html:strong', ns)
            title = strong.text

            matches = pat.match(title)

            if matches is None:
                print('invalid course list item for', school, page, title)
                continue

            school2 = matches.group(1)
            dept = matches.group(2)
            course_num = matches.group(3)

            span = li.find('html:span', ns)
            note = span.text if span is not None else ''

            br = li.findall('html:br', ns)[-1]
            desc = br.tail.strip()

            line = "{}\t{}\t{}\t{}\t{}".format(
                school2, dept, course_num, note, desc
            )

            f.write(line)
            f.write("\n")

    print('done scraping for school', school)
    f.close()
