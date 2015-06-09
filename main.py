from urllib.parse import urlencode

from pprint import pprint, pformat
from fetcher.raw_fetcher import fetch_courses, fetch_programmes, fetch_selected_semester
from generator.generator import generate
from local.saver import save


def load_conf(addr = ''):

    conf = {
        'course' : 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1',
        'programme' : 'https://wis.ntu.edu.sg/webexe/owa/aus_schedule.main'
    }

    return conf

if __name__ == '__main__':

    conf = load_conf()
    selected_semester = fetch_selected_semester(conf['programme'])
    programmes = fetch_programmes(conf['programme'])
    courses = fetch_courses(conf['course'], semester=selected_semester[1])

    course_string = '\n\nCourse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.join( map((lambda x: str(x)), courses) )
    print(course_string)

    for i in range(1, len(courses) + 1):
        print('generating {} courses... '.format(i), end='')
        result = generate(courses, i)
        print('{} results.'.format(len(result)))

        if len(result) == 0:
            print('no more plan...')
            break
