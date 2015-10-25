from django.db import models

# Create your models here.

class School(models.Model):
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=60)

    def __str__(self):
        return '{} ({})'.format(self.name, self.symbol)

class Department(models.Model):
    school = models.ForeignKey(School)
    symbol = models.CharField(max_length=2)
    name = models.CharField(max_length=60)

    def __str__(self):
        return '{} ({})'.format(self.name, self.symbol)

class Course(models.Model):
    department = models.ForeignKey(Department)
    number = models.IntegerField('course number')
    title = models.CharField('course title', max_length=200)
    description = models.TextField('course description', blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return '{} {} {}: {}'.format(
            self.department.school.symbol, self.department.symbol,
            str(self.number), self.title
        )

class Location(models.Model):
    symbol = models.CharField(max_length=16)            # e.g., "CAS", "KHC"
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return '{} ({}, {})'.format(
            self.symbol, self.latitude, self.longitude
        )

