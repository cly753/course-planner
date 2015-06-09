import re
from bs4 import BeautifulSoup
from pprint import pprint
from course.course import Course, Index, CourseTime

def parse_programmes(raw_html):
    soup = BeautifulSoup(raw_html)
    option_list = soup.select('select[name="r_course_yr"] option[value*=";"]')

    return list(map((lambda x: (x.text.strip(), x['value'])), option_list))

def parse_selected_semester(raw_html):
    soup = BeautifulSoup(raw_html)
    selected = soup.select('select[name="acadsem"] option[selected]')[0]
    return selected.text.strip(), selected['value']

def parse(raw_html):
    soup = BeautifulSoup(raw_html)

    courses_raw = list(filter((lambda x: x.name is not None and x.name == 'table'), soup.center.children))
    # pprint(courses_raw)

    courses = []
    for i in range(0, len(courses_raw), 2):
        courses.append(parse_each(courses_raw[i], courses_raw[i + 1]))
        # break
    return courses

def parse_each(raw_title, raw_index):
    # print("%%% raw_index:")
    # pprint(raw_index)

    course = parse_title(raw_title)
    all_index = parse_index(raw_index)
    course.index = all_index

    # print('\nCourse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print(str(course))

    return course


def parse_title(raw_title):
    rows = list(filter((lambda x: x.name is not None), raw_title.find_all('tr')))
    # print('%%% rows:')
    # pprint(rows)

    course = Course()
    first_row = list(map((lambda x: x.text), rows[0].find_all('td')))
    # print('%%% first row:')
    # pprint(first_row)

    course.course_code = first_row[0]
    course.course_title = first_row[1]
    course.au = int(float(first_row[2].strip().split(' ')[0]))

    # rest_row = rows[1:]
    # for r in rest_row:
    #     course.prerequisite.append(r.prettify())

    return course


def parse_index(raw_index):
    # print('hhhhhhhhhhhhhhhhhhhhhhhh')
    # pprint(raw_index)
    raw_rows = raw_index.select('tr[bgcolor^="#"]')

    all_index = []
    one_index = []
    for row in raw_rows:
        cur_row = list(map((lambda x: x.text), row.find_all('td')))
        if cur_row[0] != '' and len(one_index) > 0:
            all_index.append(parse_each_index(one_index))
            one_index = []

        one_index.append(cur_row)
    all_index.append(parse_each_index(one_index))

    return all_index


def parse_each_index(raw):
    index = Index()
    index.code = raw[0][0]
    index.course_time = list(map((lambda x: parse_each_time(x[1:])), raw))

    return index


def parse_each_time(raw):
    DAY = {
        'MON': 1,
        'TUE': 2,
        'WED': 3,
        'THU': 4,
        'FRI': 5,
        'SAT': 6,
        'SUN': 7
    }
    course_time = CourseTime()
    course_time.type = raw[0]
    course_time.group = raw[1]
    course_time.day = DAY[raw[2]]
    course_time.time = raw[3].split('-')
    course_time.venue = raw[4]

    course_time.week = list(map(lambda x: int(x), filter((lambda x: not x == ''), re.split('[\D]+', raw[5]))))
    if len(course_time.week) == 0:
        course_time.week = range(1, 14)

    # print('%%% week %%%')
    # pprint(course_time.week)

    return course_time
