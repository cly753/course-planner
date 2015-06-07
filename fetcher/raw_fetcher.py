from urllib.parse import urlencode
import urllib.request

import ssl
import socket
import http.client


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


# Override default handler

def fetch(url):
    # print('fetching from ' + url)

    urllib.request.install_opener(urllib.request.build_opener(TLS1Handler()))
    req = urllib.request.Request(url, urlencode(get_request()).encode('utf-8'))
    response = urllib.request.urlopen(req)

    text = response.read()
    # print(text)

    return text


def get_request(semester='2015;1', course_year='CE;;4;F'):
    return {
        'acadsem': semester,
        'r_course_yr': course_year,
        'r_subj_code': 'Enter Keywords or Course Code',
        'r_search_type': 'F',
        'boption': 'CLoad',
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
