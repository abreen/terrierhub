from django.db import models

# Create your models here.

class School(models.Model):
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name + ' (' + self.symbol + ')'

class Department(models.Model):
    symbol = models.CharField(max_length=2)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name + ' (' + self.symbol + ')'

class Course(models.Model):
    school = models.ForeignKey(School)
    department = models.ForeignKey(Department)
    number = models.IntegerField('course number')
    description = models.TextField('course description')
    note = models.TextField()

    def __str__(self):
        return str(self.school) + ' ' + str(self.department) + ' ' + self.number
