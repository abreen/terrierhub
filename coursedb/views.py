from django.shortcuts import render
from django.http import Http404, HttpResponse

from .models import School, Department, Course

# Create your views here.

def index(request):
    return HttpResponse('Hello.')

def school(request, school):
    try:
        s = School.objects.get(symbol__iexact=school)
    except:
        raise Http404("School does not exist")

    return HttpResponse(str(s))

def department(request, school, dept):
    try:
        s = School.objects.get(symbol__iexact=school)
    except:
        raise Http404("School does not exist")

    try:
        d = Department.objects.get(school=s, symbol__iexact=dept)
    except:
        raise Http404("Department does not exist")

    return HttpResponse(str(d))

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

    return HttpResponse(str(c))
