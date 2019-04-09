# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import base64
from base64 import b64encode
import json
from urllib import request, error

from targets.firefox.errors import TestRailError


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

    def __send_request(self, method: str, uri: str, payload=None):

        """
        :param method: HTTP Method (GET,POST)
        :param uri: TestRail URL
        :param payload: JsonObject submitted on the POST request
        :return: response Object
        """
        url = self.__url + uri
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()

        headers = {
            'Content-Type': "application/json",
            'Authorization': 'Basic %s' % auth,
            'cache-control': "no-cache"
        }

        if method == 'POST':
            api_request = request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        else:
            api_request = request.Request(url, data=None, headers=headers)

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
