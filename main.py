from functools import reduce
from pprint import pprint, pformat
from fetcher.raw_fetcher import fetch_courses, fetch_programmes, fetch_selected_semester
from generator.generator import generate
from local.databasehelper import refresh_course, find_courses_from_codes


def get_conf():
    return {
        'semester': 'https://wis.ntu.edu.sg/webexe/owa/aus_schedule.main',
        'programme': 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display',
        'course': 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1'
    }

def get_sample_courses():
    conf = get_conf()
    selected_semester = fetch_selected_semester(conf['semester'])
    programmes = fetch_programmes(conf['programme'])
    return fetch_courses(conf['course'], semester=selected_semester[1])


def print_pretty(courses):
    print(reduce((lambda x, y: x + '\n\n' + y), (map((lambda x: str(x)), courses))))


if __name__ == '__main__':
    if False:
        refresh_course(get_conf())

    codes = [ 'CE3006', 'CE4011', 'CE4022', 'CE4023', 'CZ4042', 'CZ4031' ]
    courses = find_courses_from_codes(codes)
    print_pretty(courses)

    for i in range(1, len(courses) + 1):
        result = generate(courses, i)

#
# CE4011
# CE4022
# CE4023
# CZ4042
# CZ4031
# HW0310
# CE3006
#