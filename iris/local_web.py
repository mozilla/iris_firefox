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
        try:
            SimpleHTTPRequestHandler.do_GET(self)
        except Exception, e:
            logger.info('Exception in do_GET')
            if '10053' in e:
                logger.info('Browser closed connection before response completed.')

    def do_HEAD(self):
        SimpleHTTPRequestHandler.do_HEAD(self)

    def log_message(self, format_arg, *args):
        output = ''
        for arg in args:
            output += str(arg) + '\t'
        logger.debug(output)

    def finish(self):
        try:
            SimpleHTTPRequestHandler.finish(self)
        except Exception, e:
            logger.info('Exception in finish')
            if '10053' in e:
                logger.info('Browser closed connection before response completed.')

    def handle_one_request(self):
        try:
            SimpleHTTPRequestHandler.handle_one_request(self)
        except Exception, e:
            logger.info('Exception in handle_one_request')
            if '10053' in e:
                logger.info('Browser closed connection before response completed.')



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
