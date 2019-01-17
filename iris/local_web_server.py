# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from control_center import ControlCenter


logger = logging.getLogger(__name__)
final_result = None


class CustomHandler(BaseHTTPRequestHandler):

    CONTENT_TYPES = {'htm': 'text/html', 'html': 'text/html', 'css': 'text/css',
                     'js': 'text/javascript', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                     'png': 'image/png', 'json': 'application/json', 'ico': 'image/x-icon',
                     'pdf': 'application/pdf', 'zip': 'application/zip'}

    def stop_server(self):
        logger.debug('Handler stop_server')
        LocalWebServer.ACTIVE = False

    def set_result(self, arg):
        global final_result
        final_result = arg

    @staticmethod
    def _process_path(raw_path):
        if raw_path.startswith('/?'):
            path = os.path.normpath('index.html')
        elif raw_path.endswith('/'):
            directory = os.path.normpath(raw_path[1:])
            index = os.path.join(directory, 'index.htm')
            if os.path.exists(index):
                path = index
            else:
                path = os.path.join(directory, 'index.html')
        else:
            path = os.path.normpath(raw_path[1:])
        return path

    def set_headers(self, set_content_type=True):
        logger.debug('Handler set_headers')
        self.send_response(200)
        value = 'text/html'
        if set_content_type:
            path = self._process_path(self.path)
            try:
                pos = path.rindex('.') + 1
                suffix = path[pos:]
                value = self.CONTENT_TYPES[suffix]
                logger.debug('File extension %s, content type %s' % (suffix, value))
            except IndexError:
                logger.warning('Unknown file type for resource: %s' % path)
            except ValueError:
                logger.warning('Can\'t find file extension: %s' % path)
        self.send_header('Content-Type', value)
        self.end_headers()

    def do_GET(self):
        logger.debug('Handler do_GET')
        logger.debug(self.path)
        try:
            if ControlCenter.is_command(self):
                ControlCenter.do_command(self)
            else:
                self.set_headers()
                path = self._process_path(self.path)
                f = open(path, 'rb')
                self.wfile.write(f.read())
        except Exception as e:
            logger.debug('Exception in do_GET')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def do_POST(self):
        logger.debug('Handler do_POST')
        try:
            if ControlCenter.is_command(self):
                ControlCenter.do_command(self)
            else:
                self.set_headers()
        except Exception as e:
            logger.debug('Exception in do_POSTs')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def handle_one_request(self):
        try:
            BaseHTTPRequestHandler.handle_one_request(self)
        except Exception as e:
            logger.debug('Exception in handle_one_request')
            if '10053' in e.args:
                logger.debug('Browser closed connection before response completed.')

    def finish(self):
        try:
            BaseHTTPRequestHandler.finish(self)
        except Exception as e:
            logger.debug('Exception in finish')
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
        handler = CustomHandler
        server = HTTPServer

        try:
            server_address = (self.host, self.port)
            handler.protocol_version = 'HTTP/1.0'
            httpd = server(server_address, handler)
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
