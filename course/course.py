from enum import Enum

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
        if self.day != that.day:
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

class Index:

    def __init__(self):
        self.code = '10192'
        self.course_time = []

    def __str__(self):
        return 'index: {}, \n\t{}'.format(
            self.code,
            '\n\t'.join(list(map((lambda x: str(x)), self.course_time)))
        )

    def clash(self, that):
        for t in self.course_time:
            for tt in that.course_time:
                if t.clash(tt):
                    return True
        return False

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