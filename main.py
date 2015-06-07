import fetcher.parser
import fetcher.raw_fetcher

from pprint import pprint, pformat
from generator.generator import generate
from local.saver import save


def load_conf(addr = ''):

    conf = {
        'course_url' : 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1'
        # 'course_url' : 'https://wis.ntu.edu.sg/webexe/owa/aus_schedule.main'
    }

    return conf

if __name__ == '__main__':

    conf = load_conf()
    raw_html = fetcher.raw_fetcher.fetch(conf['course_url'])
    courses = fetcher.parser.parse(raw_html)

    course_string = '\n\nCourse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.join(
        map((lambda x: str(x)), courses)
    )
    print(course_string)
    save(course_string, 'data.txt')

    result = []
    for i in range(1, len(courses) + 1):
        print('generating {} courses...'.format(i))
        result.extend(generate(courses, i))
    pprint(result)

    result = generate(courses, 4)
    save(pformat(result, 4), 'plan.txt')