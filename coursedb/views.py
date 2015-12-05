from django.shortcuts import render
from django.http import Http404, HttpResponse

from .models import School, Department, Course, Location, Section, Meeting
from .deep_scraper import scrape


def index(request):
    return render(request, 'coursedb/index.html')

def school(request, school):
    try:
        s = School.objects.get(symbol__iexact=school)
    except:
        raise Http404("School does not exist")

    departments_here = Department.objects.filter(school=s)

    context = {'school': s, 'departments': departments_here}
    return render(request, 'coursedb/school.html', context)

def department(request, school, dept):
    try:
        s = School.objects.get(symbol__iexact=school)
    except:
        raise Http404("School does not exist")

    try:
        d = Department.objects.get(school=s, symbol__iexact=dept)
    except:
        raise Http404("Department does not exist")

    courses_here = Course.objects.filter(department=d)

    context = {'school': s, 'department': d, 'courses': courses_here}
    return render(request, 'coursedb/department.html', context)

def course(request, school, dept, num):
    try:
        s = School.objects.get(symbol__iexact=school)
    except:
        raise Http404("School does not exist")

    try:
        d = Department.objects.get(school=s, symbol__iexact=dept)
    except:
        raise Http404("Department does not exist")

    try:
        c = Course.objects.get(department=d, number=int(num))
    except:
        raise Http404("Course does not exist")

    sections = scrape(c)

    for section, meetings in sections:
        # if this section already exists in the database, find it and
        # update it
        old_section = Section.objects.filter(
            course=section.course,
            section=section.section,
            start=section.start,
            end=section.end
        )

        if old_section:
            # drop all existing meetings
            old_meetings = Meeting.objects.filter(section=old_section)
            for m in old_meetings:
                m.delete()

            old_section.delete()

        section.save()

        for m in meetings:
            m.section = section
            m.save()

    sections_only = []
    for section, meetings in sections:
        section.meetings = meetings
        sections_only.append(section)

    try:
        l = Location.objects.get(symbol=s.symbol)
    except: # no location with that symbol
        l = None
        pass

    context = {
        'school': s,
        'department': d,
        'course': c,
        'sections': sections_only,
        'location': l,

        # using get() here with a default value
        'courses_added': request.session.get('courses', [])
    }

    return render(request, 'coursedb/course.html', context)

def api(request, function):
    if function == 'add_course':
        to_add = {
            'school': request.GET['school'],
            'department': request.GET['department'],
            'number': request.GET['number'],
            'section': request.GET['section'],
            'startend': request.GET['startend']
        }

        if 'courses' not in request.session:
            request.session['courses'] = [to_add]

        elif to_add not in request.session['courses']:
            current_courses = request.session['courses']
            current_courses.append(to_add)

            # editing current_courses in-place doesn't seem to work
            # instead, we set the reference here
            request.session['courses'] = current_courses

    elif function == 'clear_courses':
        request.session['courses'] = []

    else:
        return HttpResponse('invalid API function')

    return HttpResponse('')

def schedule(request):
    saved = []
    rowid = 0

    for section_dict in request.session['courses']:
        school = section_dict['school']
        department = section_dict['department']
        number = section_dict['number']
        section = section_dict['section']
        startend = section_dict['startend']

        try:
            s = School.objects.get(symbol__iexact=school)
        except:
            raise Http404("School does not exist")

        try:
            d = Department.objects.get(school=s, symbol__iexact=department)
        except:
            raise Http404("Department does not exist")

        try:
            c = Course.objects.get(department=d, number=int(number))
        except:
            raise Http404("Course does not exist")

        starting, ending = Section.startend_from_string(startend)
        sec = Section.objects.get(
            course=c,
            section__iexact=section,
            start=starting,
            end=ending
        )

        meetings = Meeting.objects.filter(
            section=sec
        )

        rowid += 1
        clazz = {}

        clazz['rowid'] = 'row' + str(rowid)
        clazz['school'] = s.symbol
        clazz['department'] = d.symbol
        clazz['number'] = c.number
        clazz['section'] = sec.section

        meeting0 = meetings[0]

        clazz['building'] = meeting0.building.symbol
        clazz['room'] = meeting0.room
        clazz['days'] = meeting0.days_as_string()

        clazz['time'] = str(meeting0.start.hour % 12) + ':' + \
                meeting0.start.strftime('%M %p') + '-' + \
                str(meeting0.end.hour % 12) + ':' + \
                meeting0.end.strftime('%M %p')

        clazz['daysarray'] = []
        days_list = Meeting.days_from_int(meeting0.days)
        for day in days_list:
            for day_abbrev, i, _ in Meeting.DAYS:
                if day == day_abbrev:
                    clazz['daysarray'].append(i)
                    break
            else:
                raise ValueError()

        start = meeting0.start
        end = meeting0.end

        clazz['start_hour'] = start.hour
        if start.minute > 0:
            clazz['start_hour'] += start.minute / 60

        clazz['mins'] = (end.hour * 60 + end.minute) - \
                (start.hour * 60 + start.minute)

        saved.append(clazz)

    return render(request, 'coursedb/schedule.html', {'saved_classes': saved})
