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
        to_add = request.GET['course_to_add']

        if 'courses' not in request.session:
            request.session['courses'] = [to_add]

        elif to_add not in current_courses:
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
    return render(request, 'coursedb/schedule.html', {})

