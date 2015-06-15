from enum import Enum
import json


class Type(Enum):
    LEC = 1
    TUT = 2
    LAB = 3

class CourseTime:

    def __init__(self):
        self.type = ''
        self.group = ''
        self.day = -1

        self.time = []

        self.venue = ''
        self.week = [1, 3, 5]

    def clash(self, that):
        if self.day == 0 or self.day != that.day:
            return False

        if len(set(self.week) & set(that.week)) == 0:
            return False

        if self.time[0] < that.time[1] and self.time[1] > that.time[0]:
            return True
        return False

    def __str__(self):
        return 'type: {}, group: {}, day: {}, time: {}-{}, venue: {}, week: {}'.format(
            self.type,
            self.group,
            self.day,
            self.time[0],
            self.time[1],
            self.venue,
            ','.join(map(lambda x: str(x), self.week))
        )

    def to_json(self):
        return {
            'type': self.type,
            'group': self.group,
            'day': self.day,
            'time': self.time,
            'venue': self.venue,
            'week': self.week
        }

class Index:

    def __init__(self):
        self.index = '10192'
        self.course_time = []

    def __str__(self):
        return 'index: {}, \n\t{}'.format(
            self.index,
            '\n\t'.join(list(map((lambda x: str(x)), self.course_time)))
        )

    def clash(self, that):
        for t in self.course_time:
            for tt in that.course_time:
                if t.clash(tt):
                    return True
        return False

    def to_json(self):
        return {
            'index': self.index,
            'course_time': list(map((lambda x: x.to_json()), self.course_time))
        }

class Course:

    def __init__(self):
        self.course_code = ''
        self.course_title = ''
        self.au = -777
        self.prerequisite = []

        self.index = []

    def __str__(self):
        return 'course code: {}, {}, au: {}, prerequisite: {}, index: \n{}'.format(
            self.course_code,
            self.course_title,
            self.au,
            ','.join(self.prerequisite),
            '\n'.join(list(map((lambda x: str(x)), self.index)))
        )

    def to_json(self):
        return {
            'course_code': self.course_code,
            'course_title': self.course_title,
            'au': self.au,
            'prerequisite': self.prerequisite,
            'index': list(map((lambda x: x.to_json()), self.index))
        }

def course_time_from_json(js):
    course_time = CourseTime()

    course_time.type = js['type']
    course_time.group = js['group']
    course_time.day = js['day']
    course_time.time = js['time']
    course_time.venue = js['venue']
    course_time.week = js['week']

    return course_time

def index_from_json(js):
    index = Index()

    index.index = js['index']
    index.course_time = [ course_time_from_json(j) for j in js['course_time'] ]

    return index

def course_from_json(js):
    course = Course()

    course.course_code = js['course_code']
    course.course_title = js['course_title']
    course.au = js['au']
    course.prerequisite = js['prerequisite']
    course.index = [ index_from_json(j) for j in js['index'] ]

    return course
