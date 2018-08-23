# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import logging


logger = logging.getLogger(__name__)


class ControlCenter(object):

    COMMANDS = ['delete', 'finish']

    @staticmethod
    def is_command(request):
        server_host, server_port = request.server.server_address
        client_host, client_port = request.client_address

        # First verify that the request is local, for security reasons.
        if server_host == client_host:
            # Then examine the path for command keywords
            found = False
            for command in ControlCenter.COMMANDS:
                if request.path.startswith('/%s' % command):
                    found = True
            return found
        return False

    @staticmethod
    def do_command(request):
        print 'do_command: %s ' % request.path
        if 'delete' in request.path:
            try:
                ControlCenter.delete(request.path.split('?')[1])
            except KeyError:
                logger.error('Malformed delete command: %s' % request.path)
        elif 'finish' in request.path:
            ControlCenter.finish(request)
        return True

    @staticmethod
    def delete(args):
        """
        Take args, construct path to run directory and delete it
        Import libraries as needed
        """
        print 'delete: %s ' % args
        pass

    @staticmethod
    def finish(request):
        """
        Find POST body, handle JSON in body
        """
        print 'finish: %s' % request.path
        request.set_result('a new beginning')
        request.stop_server()
        return
