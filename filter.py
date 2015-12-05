from django.db import models
from .models import School, Department, Course, Location, Section, Meeting


s = []
results = .GET(s)

#School

def q1(str):
    x = s[0]
    resultsS = School.objects.filter(symbol__iexact = x)

#Department

def q2(str):
    x = s[1]
    resultsD = Department.objects.filter(symbol__iexact = x)

#Course

def q3(str):
    x = s[2]
    resultsC = Course.objects.filter(symbol__iexact = x)

def tok_id(s):
    return [s]

def tok_split(s):
    return s.split()

def search(tokenizers, queriers, s):
    token_lists [] 
    for tok in tokenizers:
        token_list.append(tok(s))
        qsets = []
        for token_list in token_lists:
            for t in token_list:
	        for q in queries:
		    qsets.append(q(t))

def sort(x):
    return max(x)




















