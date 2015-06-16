from functools import reduce
import itertools
from pprint import pprint
from local.databasehelper import find_courses_from_codes


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
                    if semester[w - 1][h] == 1:
                        return False
                    semester[w - 1][h] = 1
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

    # itertools.product
    # [
    #     [
    #         (course_code_1, index_1),
    #         (course_code_2, index_1)
    #     ],
    #     [
    #         (course_code_1, index_1),
    #         (course_code_2, index_2)
    #     ],
    #     [
    #         (course_code_1, index_1),
    #         (course_code_2, index_3)
    #     ],
    #     ...
    # ]

    return list(filter((lambda x: check22(list(map((lambda x: x[1]), x)))), list(itertools.product(*flat_courses))))


def generate(courses, n):

    # [
    #     [
    #         (course_code_1, index_1),
    #         (course_code_1, index_2)
    #     ],
    #     [
    #         (course_code_2, index_1),
    #         (course_code_2, index_2),
    #         (course_code_2, index_3)
    #     ],
    #     ...
    # ]

    flat_courses = []
    for c in courses:
        flat = []
        for i in c.index:
            flat.append((c.course_code, i))
        flat_courses.append(flat)

    # for c in flat_courses:
    #     for i in c:
    #         print('flat {} - {}'.format(i[0], i[1].index))

    all_result = []
    for x in itertools.combinations(flat_courses, n):

        # [
        #     [
        #         (course_code_1, index_1),
        #         (course_code_1, index_2)
        #     ]
        # ]

        result = generate_index(x)
        all_result.extend(result)

        xxx = ''
        for xx in x:
            xxx += xx[0][0] + ' '

        # xxx = reduce((lambda xx, yy: xx[0][0] + ' ' + yy[0][0]), x, [('', '')])
        # print('what??? ' + str(xxx))

        print('{} courses: {}'.format(n, xxx))
        if len(result) == 0:
            print('result 0\n')
            continue

        print('result:')
        for each in result:
            for ci in each:
                print('\t{} - {}'.format(ci[0], ci[1].index))
            print()
        print()
    return all_result


def generate_from_codes(courses_codes, n):
    return generate(find_courses_from_codes(courses_codes), n)
