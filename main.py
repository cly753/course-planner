from urllib.parse import urlencode

from pprint import pprint, pformat
from pymongo import MongoClient
from course.course import course_from_json
from fetcher.raw_fetcher import fetch_courses, fetch_programmes, fetch_selected_semester
from generator.generator import generate
from local.databasehelper import refresh_course
from local.saver import save


def load_conf(addr = ''):

    conf = {
        'course' : 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1',
        'semester' : 'https://wis.ntu.edu.sg/webexe/owa/aus_schedule.main',
        'programme' : 'https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display'
    }

    return conf

def get_courses():
    conf = load_conf()
    selected_semester = fetch_selected_semester(conf['programme'])
    programmes = fetch_programmes(conf['programme'])

    courses = fetch_courses(conf['course'], semester=selected_semester[1])

    return courses

def test():
    courses = get_courses()

    course_string = '\n\nCourse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.join( map((lambda x: str(x)), courses) )
    print(course_string)

    for i in range(1, len(courses) + 1):
        print('generating {} courses... '.format(i), end='')
        result = generate(courses, i)
        print('{} results.'.format(len(result)))

        if len(result) == 0:
            print('no more plan...')
            break

def testDB():
    client = MongoClient('localhost', 27017)
    db = client.testDB
    collection = db.testCollection
    collection.drop()

    # doc = { 'name': 'world', 'action': 'hello' };
    # collection.insert_one(doc)

    courses = get_courses()
    courses_json = list(map((lambda x: x.to_json()), courses))
    collection.insert_many(courses_json)

    pprint(db.collection_names(include_system_collections=False))
    coursesccc = []
    for x in collection.find({"au": {"$gt": 0}}):
        print(x)
        coursesccc.append(course_from_json(x))

    course_string = '\n\nCourse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.join( map((lambda x: str(x)), coursesccc) )
    print(course_string)

def testHelper():
    refresh_course(load_conf())

if __name__ == '__main__':
    # test()

    # testDB()

    testHelper()