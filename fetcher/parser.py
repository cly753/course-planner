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
    all_semester = soup.select('select[name="acadsem"] option')
    selected = all_semester[0]
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

    course.course_code = first_row[0].upper()
    course.course_title = first_row[1]
    course.au = int(float(first_row[2].strip().split(' ')[0]))

    # rest_row = rows[1:]
    # for r in rest_row:
    #     course.prerequisite.append(r.prettify())

    return course


def parse_index(raw_index):
    raw_rows = raw_index.select('tr[bgcolor^="#"]')

    if len(raw_rows) == 0:
        return []

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
    index.index = raw[0][0]
    index.course_time = list(map((lambda x: parse_each_time(x[1:])), raw))

    return index


def parse_each_time(raw):
    DAY = {
        'NONE': 0,
        'MON': 1,
        'TUE': 2,
        'WED': 3,
        'THU': 4,
        'FRI': 5,
        'SAT': 6,
        'SUN': 7
    }
    course_time = CourseTime()
    course_time.type = raw[0] if not raw[0] == '\xa0' else 'NoType'
    course_time.group = raw[1] if not raw[1] == '\xa0' else 'NoGroup'
    course_time.day = DAY[raw[2]] if not raw[2] == '\xa0' else 0
    course_time.time = raw[3].split('-') if not raw[3] == '\xa0' else ['0000', '0000']
    course_time.venue = raw[4] if not raw[4] == '\xa0' else 'NoVenue'

    if len(raw[5]) < 3:
        course_time.week = list(range(1, 14))
    else:
        try:
            course_time.week = []
            temp_week = list(filter((lambda x: not x == ''), re.split('[^0-9\-]+', raw[5])))
            for w in temp_week:
                if '-' in w:
                    ab = w.split('-')
                    a = int(ab[0])
                    b = int(ab[1])
                    course_time.week.extend(list(range(a, b + 1)))
                else:
                    course_time.week.append(int(w))
        except ValueError as e:
            course_time.week = []
            print('Exception when parsing week: "{}", treated as []...details:\n{}'.format(raw[5], str(e)))

    # print('%%% week %%%')
    # pprint(course_time.week)

    return course_time
