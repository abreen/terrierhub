from django.db import models

# Create your models here.

class School(models.Model):
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.symbol

class Department(models.Model):
    school = models.ForeignKey(School)
    symbol = models.CharField(max_length=2)
    name = models.CharField(max_length=60)

    def __str__(self):
        return str(self.school) + ' ' + self.symbol

class Course(models.Model):
    department = models.ForeignKey(Department)
    number = models.IntegerField('course number')
    description = models.TextField('course description', blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.department) + ' ' + str(self.number)
