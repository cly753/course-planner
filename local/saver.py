
import json
import os

def save_string(course_string, destination):
    absolute_path = os.path.abspath(destination)
    path = os.path.dirname(absolute_path)
    if not os.path.exists(path):
        raise Exception('Path does not exist: ' + path)

    with open(absolute_path, 'w') as f:
        f.write(course_string)
        f.write('\n')

def save(courses, destination):
    pretty = json.dumps(courses)

    absolute_path = os.path.abspath(destination)
    path = os.path.dirname(absolute_path)
    if not os.path.exists(path):
        raise Exception('Path does not exist: ' + path)

    with open(absolute_path, 'w') as f:
        f.write(pretty)
        f.write('\n')