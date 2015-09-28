from django.shortcuts import render
from django.http import Http404, HttpResponse

from .models import School, Department, Course

# Create your views here.

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

    context = {'school': s, 'department': d, 'course': c}
    return render(request, 'coursedb/course.html', context)
