from pymongo import MongoClient
from fetcher.raw_fetcher import fetch_all_courses

def refresh_course(conf):
    client = MongoClient('localhost', 27017)
    db = client.testDB
    collection = db.testCollection
    collection.drop()

    all_courses = fetch_all_courses(conf)

    courses_json = list(map((lambda x: x.to_json()), all_courses))
    collection.insert_many(courses_json)

    return True

def find_courses_from_codes(course_codes):
    pass