# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from control_center import ControlCenter as cc


logger = logging.getLogger(__name__)

final_result = None


class CustomHandler(SimpleHTTPRequestHandler):

    # The main purpose of this class is to override several superclass methods, in order to
    # prevent undesired error messages from appearing in the console. The HTTPServer used here
    # raises an exception if the client closes the connection while the server is still
    # sending data. For our purposes, this behavior is not important, so we just want to ignore
    # the dropped connection and suppress the error message.

    def stop_server(self):
        LocalWebServer.ACTIVE = False

    def set_result(self, arg):
        global final_result
        final_result = arg

    def do_GET(self):
        global final_result

        try:
            if cc.is_command(self):
                cc.do_command(self)
                self.send_response(200)
            else:
                SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            logger.debug('Exception in do_GET')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def do_HEAD(self):
        try:
            SimpleHTTPRequestHandler.do_HEAD(self)
        except Exception as e:
            logger.debug('Exception in do_HEAD')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def finish(self):
        try:
            SimpleHTTPRequestHandler.finish(self)
        except Exception as e:
            logger.debug('Exception in finish')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def handle_one_request(self):
        try:
            SimpleHTTPRequestHandler.handle_one_request(self)
        except Exception as e:
            logger.debug('Exception in handle_one_request')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def log_message(self, format_arg, *args):
        # Eliminate the default output from the HTTP server unless we are in debug mode.
        output = ''
        for arg in args:
            output += str(arg) + '\t'
        logger.debug(output)


class LocalWebServer(object):

    ACTIVE = True

    def __init__(self, path, port):
        LocalWebServer.ACTIVE = True
        self.port = port
        self.web_root = path
        self.host = '127.0.0.1'
        self.result = None
        self.start()

    def stop(self):
        LocalWebServer.ACTIVE = False

    def start(self):
        global final_result

        os.chdir(self.web_root)
        handler = SimpleHTTPRequestHandler
        server = HTTPServer

        try:
            server_address = (self.host, self.port)
            handler.protocol_version = 'HTTP/1.0'
            httpd = server(server_address, CustomHandler)
            sock_name = httpd.socket.getsockname()
            logger.info('Serving HTTP on %s port %s.' % (sock_name[0], sock_name[1]))
            while LocalWebServer.ACTIVE:
                httpd.handle_request()
            self.result = final_result
            return
        except IOError:
            raise IOError('Unable to open port %s on %s' % (self.port, self.host))
        except TypeError as e:
            # Ignore intermittent error message during process shutdown.
            error_string = 'cleanup_handler() takes no arguments (2 given)'
            if error_string in e.args:
                logger.debug('Unable to call server cleanup handler')
            else:
                raise TypeError(e.args)
