# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
import socket
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

    def send_header(self, keyword, value):
        """Send a MIME header."""
        try:
            if self.request_version != 'HTTP/0.9':
                self.wfile.write("%s: %s\r\n" % (keyword, value))

            if keyword.lower() == 'connection':
                if value.lower() == 'close':
                    self.close_connection = 1
                elif value.lower() == 'keep-alive':
                    self.close_connection = 0
        except Exception, e:
            # Errno 10053 is to be ignored, as the browser connection closes before
            # the server's response is sent, causing an error
            logger.info(e)
            if '10053' in e:
                logger.info('Browser closed connection before response completed.')

    def finish(self):
        """
        This comes from StreamRequestHandler, except the part where we call close().
        We wish to capture a specific exception that happens primarily on
        Windows, and essentially ignore it.
        """
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                # An final socket error may have occurred here, such as
                # the local error ECONNABORTED.
                pass
        try:
            self.wfile.close()
            self.rfile.close()
        except Exception, e:
            # Errno 10053 is to be ignored, as the browser connection closes before
            # the server's response is sent, causing an error
            logger.info(e)
            if '10053' in e:
                logger.info('Browser closed connection before response completed.')

    def handle_one_request(self):
        """
        This comes from BaseHTTPRequest, except the part where we call flush().
        We wish to capture a specific exception that happens primarily on
        Windows, and essentially ignore it.
        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            try:
                self.wfile.flush() #actually send the response if not already done.
            except Exception, e:
                # Errno 10053 is to be ignored, as the browser connection closes before
                # the server's response is sent, causing an error
                if '10053' in e:
                    logger.info('Browser closed connection before response completed.')
        except socket.timeout, e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return


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
