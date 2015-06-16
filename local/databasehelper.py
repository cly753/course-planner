from pprint import pprint
from pymongo import MongoClient
from course.course import course_from_json
from fetcher.raw_fetcher import fetch_all_courses


def get_collection():
    client = MongoClient('localhost', 27017)
    db = client.testDB
    collection = db.testCollection
    return collection


def refresh_course(conf):
    all_courses = fetch_all_courses(conf)
    courses_json = list(map((lambda x: x.to_json()), all_courses))

    collection = get_collection()
    collection.drop()
    collection.insert_many(courses_json)

    return all_courses

def find_courses_from_codes(course_codes):
    collection = get_collection()

    found = []
    found_code = set()
    for code in course_codes:
        course_json = collection.find({'course_code': code.upper()})
        for cj in course_json:
            if not cj['course_code'] in found_code:
                found_code.add(cj['course_code'])
                course = course_from_json(cj)
                found.append(course)
    return found
