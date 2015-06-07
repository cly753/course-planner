
import json
import os
import course

def load(source):

    absolute_path = os.path.abspath(source)

    if not os.path.isfile(absolute_path):
        raise Exception('File does not exist: ' + absolute_path)

    with open(absolute_path, 'r') as f:
        pretty = f.read()

    courses_json = json.loads(pretty)
    courses = [ course.Course(c) for c in courses_json ]

    return courses