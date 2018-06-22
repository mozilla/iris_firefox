# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


class CustomHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        SimpleHTTPRequestHandler.do_HEAD(self)

    def log_message(self, format_arg, *args):
        output = ''
        for arg in args:
            output += str(arg) + '\t'
        logger.debug(output)


class LocalWebServer(object):

    def __init__(self, path, port):
        self.port = port
        self.web_root = path
        self.host = '127.0.0.1'
        self.start()

    def start(self):
        os.chdir(self.web_root)
        handler = SimpleHTTPRequestHandler
        server = HTTPServer

        try:
            server_address = (self.host, self.port)
            handler.protocol_version = 'HTTP/1.0'
            httpd = server(server_address, CustomHandler)
            sock_name = httpd.socket.getsockname()
            logger.info('Serving HTTP on %s port %s.' % (sock_name[0], sock_name[1]))
            httpd.serve_forever()
        except:
            raise IOError('Unable to open port %s on %s' % (self.port, self.host))
