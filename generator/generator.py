import itertools
from pprint import pprint


def time_to_int(time):
    return int(time[0:2]) * 2 + 1 if int(time[2:4]) > 0 else 0

def check(indexs):
    week = 13
    half_hour = 48
    semester = [[0 for x in range(half_hour)] for x in range(week)]

    for index in indexs:
        for t in index.course_time:
            for w in t.week:
                for h in range(time_to_int(t.time[0]), time_to_int(t.time[1])):
                    if semester[w-1][h] == 1:
                        return False
                    semester[w-1][h] = 1
    return True

def check22(indexs):
    for two2 in itertools.combinations(indexs, 2):
        if two2[0].clash(two2[1]):
            return False
    return True

def generate_index(flat_courses):
    # print('%%% flat_courses %%%')
    # pprint(flat_courses)
    # all_possible = list(itertools.product(*flat_courses))
    # print('%%% all_possible %%%')
    # pprint(all_possible)

    result = list(filter((lambda x: check22(list(map((lambda x: x[1]), x)))), list(itertools.product(*flat_courses))))
    return result

def generate(courses, n):
    flat_courses = []
    for c in courses:
        flat_course = []
        for i in c.index:
            flat_course.append((c.course_code, i))
        flat_courses.append(flat_course)

    result = []
    for x in itertools.combinations(flat_courses, n):
        result.extend(generate_index(x))
    return result