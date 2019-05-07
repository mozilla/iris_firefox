# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import logging
import os
import shutil

from src.core.util.path_manager import PathManager


logger = logging.getLogger(__name__)
COMMANDS = ['delete', 'go', 'cancel']


def is_command(request):
    server_host, server_port = request.server.server_address
    client_host, client_port = request.client_address

    # First verify that the request is local, for security reasons.
    if server_host == client_host:
        # Then examine the path for command keywords
        found = False
        for command in COMMANDS:
            if request.path.startswith('/%s' % command):
                found = True
        return found
    return False


def do_command(request):
    logger.debug('Parsing command from path: %s ' % request.path)
    if 'delete?' in request.path:
        try:
            request.set_headers(False)
            delete(request.path.split('?')[1])
        except KeyError:
            logger.error('Malformed delete command: %s' % request.path)
    elif 'deleteAll' in request.path:
        delete_all()
    elif 'go' in request.path:
        go(request)
        request.set_headers(False)
    elif 'cancel' in request.path:
        cancel(request)
        request.set_headers(False)
    return True


def delete(args, update_run_file=True):
    """
    Delete a past run.
    :param args: The run ID to delete
    :param update_run_file: Remove entry from runs.json file
    """
    logger.debug('Received delete command with arguments: %s ' % args)

    if update_run_file:
        # Load run log JSON, find entry that matches the argument and delete it.
        # Then, write new run log file.
        run_file = os.path.join(PathManager.get_working_dir(), 'data', 'runs.json')
        if os.path.exists(run_file):
            logger.debug('Deleting entry %s from run file: %s' % (args, run_file))
            with open(run_file, 'r') as data:
                run_file_data = json.load(data)
            found = False
            for run in run_file_data['runs']:
                if run['id'] == args:
                    run_file_data['runs'].remove(run)
                    found = True
            if found:
                with open(run_file, 'w') as data:
                    json.dump(run_file_data, data, sort_keys=True, indent=True)
            else:
                logger.error('Entry for run %s not found in run log file.' % args)
        else:
            logger.error('Run file not found.')

    # Remove run directory on disk.
    target_run = os.path.join(PathManager.get_working_dir(), 'runs', args)
    if os.path.exists(target_run):
        shutil.rmtree(target_run, ignore_errors=True)
    else:
        logger.debug('Run directory does not exist: %s' % target_run)


def delete_all():
    """
    Delete each run in the runs.json file, one at a time.
    """
    logger.debug('Delete All command received.')
    run_file = os.path.join(PathManager.get_working_dir(), 'data', 'runs.json')

    with open(run_file, 'r') as data:
        run_file_data = json.load(data)
        data.close()

    for run in run_file_data['runs']:
            delete(run['id'])


def go(request):
    """
    Find POST body, handle JSON in body.
    """
    logger.debug('Finish command received: %s' % request.path)
    data_string = request.rfile.read(int(request.headers['Content-Length'])).decode('utf-8')
    logger.debug(data_string)
    sorted_response = json.dumps(json.loads(data_string), sort_keys=True)
    request.set_result(json.loads(sorted_response))
    request.stop_server()
    return


def cancel(request):
    """
    Stop web server with no further action.
    """
    logger.debug('Cancel command received: %s' % request.path)
    request.set_result('cancel')
    request.stop_server()
    return
