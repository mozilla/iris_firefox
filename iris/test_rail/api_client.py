# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import urllib2, json, base64
from iris.api.core.errors import *


class APIClient:
    def __init__(self, url):
        self.user = ''
        self.password = ''
        self.__url = url

    def send_get(self, uri):

        """
        :param uri: TestRail URL
        :return: response Object
        """
        return self.__send_request('GET', uri, None)

    def send_post(self, uri, data):

        """
        :param uri: TestRail URL
        :param data: Object submitted on the POST request
        :return: response Object
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, payload):

        """
        :param method: HTTP Method (GET,POST)
        :param uri: TestRail URL
        :param payload: JsonObject submitted on the POST request
        :return: response Object
        """
        url = self.__url + uri
        api_request = urllib2.Request(url)
        if method == 'POST':
            api_request.add_data(json.dumps(payload))
        auth = base64.b64encode('%s:%s' % (self.user, self.password))

        api_request.add_header('Authorization', 'Basic %s' % auth)
        api_request.add_header('Content-Type', 'application/json')

        try:
            response = urllib2.urlopen(api_request).read()
        except urllib2.HTTPError as e:
            response = e.read()
            raise TestRailError('TestRail API returned HTTP %s (%s)' %
                   (e.code, response))
        else:
            if response:
                result = json.loads(response)
            else:
                result = {}

        return result
