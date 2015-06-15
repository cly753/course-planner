from pprint import pprint
from urllib.parse import urlencode
import urllib.request

import ssl
import socket
import http.client
from fetcher import parser
from fetcher.parser import parse_programmes, parse_selected_semester


class TLS1Connection(http.client.HTTPSConnection):
    """Like HTTPSConnection but more specific"""

    def __init__(self, host, **kwargs):
        http.client.HTTPSConnection.__init__(self, host, **kwargs)

    def connect(self):
        """Overrides HTTPSConnection.connect to specify TLS version"""
        # Standard implementation from HTTPSConnection, which is not
        # designed for extension, unfortunately
        sock = socket.create_connection((self.host, self.port),
                                        self.timeout, self.source_address)
        if getattr(self, '_tunnel_host', None):
            self.sock = sock
            self._tunnel()

        # This is the only difference; default wrap_socket uses SSLv23
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                    ssl_version=ssl.PROTOCOL_TLSv1)


class TLS1Handler(urllib.request.HTTPSHandler):
    """Like HTTPSHandler but more specific"""

    def __init__(self):
        urllib.request.HTTPSHandler.__init__(self)

    def https_open(self, req):
        return self.do_open(TLS1Connection, req)

def fetch_post(url, data):
    urllib.request.install_opener(urllib.request.build_opener(TLS1Handler()))
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)

    return response.read()

def fetch_get(url):
    urllib.request.install_opener(urllib.request.build_opener(TLS1Handler()))
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)

    return response.read()

def get_request(semester='2015;1', course_year='CE;;4;F', boption='x'):
    return {
        'acadsem': semester,
        'r_course_yr': course_year,
        'r_subj_code': 'Enter Keywords or Course Code',
        'r_search_type': 'F',
        'boption': boption,
        'acadsem': semester,
        'staff_access': 'false'
    }

    # return {
    #     'acadsem': '2015;1',
    #     'r_course_yr':'CE;;4;F',
    #     'r_subj_code':'Enter Keywords or Course Code',
    #     'r_search_type':'F',
    #     'boption':'CLoad',
    #     'acadsem':'2015;1',
    #     'staff_access':'false'
    # }

def fetch_all_courses(conf):
    semester = fetch_selected_semester(conf['semester'])
    programmes = fetch_programmes(conf['programme'])

    print('semester: {}', semester)
    print('programmes... total: {}', len(programmes))

    all_courses = []
    for i in range(0, len(programmes)):
        print('fetching {}/{}'.format(i + 1, len(programmes)))
        pro = programmes[i]
        courses = fetch_courses(conf['course'], semester[1], pro[1])
        for c in courses:
            pprint(c.to_json())
        all_courses.extend(courses)

    return all_courses

def fetch_courses(url, semester='2015;1', course_year='CE;;4;F'):
    print('fetch_courses... url: {}, semester: {}, course_year: {}, data:'.format(url, semester, course_year))
    data = get_request(semester, course_year, 'CLoad')
    pprint(data)
    raw_html = fetch_post(url, urlencode(data).encode('utf-8'))
    print('response: {}', raw_html)

    courses = parser.parse(raw_html)
    return courses

def fetch_programmes(url, semester='2015;1'):
    print('fetch_programmes... url: {}, semester: {}, data:'.format(url, semester))
    data = get_request(semester, '', 'x')
    pprint(data)
    raw_html = fetch_post(url, urlencode(data).encode('utf-8'))
    print('response: {}', raw_html)
    return parse_programmes(raw_html)

def fetch_selected_semester(url):
    return parse_selected_semester(fetch_get(url))