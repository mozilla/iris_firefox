# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import base64
import json
from urllib import request, error

from src.core.api.errors import TestRailError


class APIClient:
    def __init__(self, url: str):
        self.user = ''
        self.password = ''
        self.__url = url

    def send_get(self, uri: str):

        """
        :param uri: TestRail URL
        :return: response Object
        """
        return self.__send_request('GET', uri)

    def send_post(self, uri: str, data):

        """
        :param uri: TestRail URL
        :param data: Object submitted on the POST request
        :return: response Object
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method: str, uri: str, payload: str = None):

        """
        :param method: HTTP Method (GET,POST)
        :param uri: TestRail URL
        :param payload: JsonObject submitted on the POST request
        :return: response Object
        """
        url = self.__url + uri

        if method == 'POST':
            api_request = request.Request(url, data=json.dumps(payload))
        else:
            api_request = request.Request(url)
        auth = base64.b64encode('%s:%s' % (self.user, self.password))

        api_request.add_header('Authorization', 'Basic %s' % auth)
        api_request.add_header('Content-Type', 'application/json')

        try:
            response = request.urlopen(api_request).read()
        except error.HTTPError as e:
            response = e.read()
            raise TestRailError('TestRail API returned HTTP %s (%s)' %
                                (e.code, response))
        else:
            if response:
                result = json.loads(response)
            else:
                result = {}

        return result
