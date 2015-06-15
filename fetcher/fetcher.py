import requests

import ssl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

# class Ssl1HttpAdapter(HTTPAdapter):
#     """"Transport adapter" that allows us to use SSLv1.0."""
#
#     def init_poolmanager(self, connections, maxsize, block=False):
#         self.poolmanager = PoolManager(num_pools=connections,
#                                        maxsize=maxsize,
#                                        block=block,
#                                        ssl_version=ssl.PROTOCOL_TLSv1)
#
# def get_Ssl1_session():
#     s = requests.Session()
#     s.mount('https://', Ssl1HttpAdapter())
#
#     return s
#
# def fetch(url):
#     # print('fetching from ' + url)
#
#     s = get_Ssl1_session()
#     r = s.get(url, verify=False)
#
#     print(r.text)
#
#     pass