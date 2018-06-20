# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


class LocalWeb(object):

    def __init__(self, port):
        self.port = port
        self.web_root = __file__.split('.py')[0]
        self.start()

    def start(self):
        os.chdir(self.web_root)
        HandlerClass = SimpleHTTPRequestHandler
        ServerClass = BaseHTTPServer.HTTPServer

        server_address = ('127.0.0.1', self.port)

        HandlerClass.protocol_version = 'HTTP/1.0'
        httpd = ServerClass(server_address, HandlerClass)

        sa = httpd.socket.getsockname()
        logger.info('Serving HTTP on %s port %s ...' % (sa[0], sa[1]))
        httpd.serve_forever()
