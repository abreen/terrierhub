from django.db import models

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

class Section(models.Model):
    INSTRUCTION_TYPES = (
        ('APP', 0, 'applied art'),
        ('DIS', 1, 'discussion section'),
        ('DRS', 2, 'directed study'),
        ('EXP', 3, 'clinical experience'),
        ('IND', 4, 'independent course'),
        ('LAB', 5, 'laboratory'),
        ('LEC', 6, 'lecture'),
        ('OTH', 7, 'other'),
        ('PLB', 8, 'pre-lab section')
    )

    def type_from_int(i):
        return Section.INSTRUCTION_TYPES[i]

    def type_to_int(symbol):
        for s, i, _ in Section.INSTRUCTION_TYPES:
            if s == symbol:
                return i

        raise ValueError('invalid instruction type symbol')

    course = models.ForeignKey(Course)
    section = models.CharField(max_length=40)               # e.g., 'A2'
    open_seats = models.IntegerField('open seats', null=True)
    instructor = models.CharField('instructor', max_length=200)
    type = models.IntegerField(choices=tuple([(t[1], t[2]) for t in INSTRUCTION_TYPES]))
    notes = models.CharField(default='', blank=True, max_length=600)

    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return str(self.course) + ' ' + self.section

class Meeting(models.Model):
    DAYS = (
        ('M', 0, 'Monday'),
        ('T', 1, 'Tuesday'),
        ('W', 2, 'Wednesday'),
        ('R', 3, 'Thursday'),
        ('F', 4, 'Friday'),
        ('S', 5, 'Saturday'),
        ('U', 6, 'Sunday')
    )

    def days_to_int(days):
        valid_letters = [d[0] for d in Meeting.DAYS]
        n = 0
        for d in days:
            if d not in valid_letters:
                raise ValueError('invalid day letter specified')
            else:
                n |= 1 << valid_letters.index(d)
        return n

    def days_from_int(n):
        valid_letters = [d[0] for d in Meeting.DAYS]
        days = []
        for i in range(7):
            mask = 1 << i
            if n & mask:
                days.append(valid_letters[i])

        return days

    def days_as_string(self):
        return ''.join(Meeting.days_from_int(self.days))

    section = models.ForeignKey(Section)
    days = models.IntegerField()

    start = models.TimeField()
    end = models.TimeField()

    start_date = models.DateField()
    end_date = models.DateField()

    building = models.ForeignKey(Location, null=True)
    room = models.CharField(max_length=40, null=True)

    def __str__(self):
        return '{} {}, {} {}-{} (for section {})'.format(
            str(self.building), self.room,
            ''.join(Meeting.days_from_int(self.days)),
            str(self.start), str(self.end), str(self.section)
        )
