# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

import coloredlogs

from src.core.util.arg_parser import get_core_args
from src.core.util.path_manager import PathManager

LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'

SUCCESS_LEVEL_NUM = 35
logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')

logger = logging.getLogger(__name__)

coloredlogs.DEFAULT_LOG_FORMAT = LOG_FORMAT
coloredlogs.DEFAULT_FIELD_STYLES = {'levelname': {'color': 'cyan', 'bold': True},
                                    'name': {'color': 'cyan', 'bold': True}}
coloredlogs.DEFAULT_LEVEL_STYLES = {'warning': {'color': 'yellow', 'bold': True},
                                    'success': {'color': 'green', 'bold': True},
                                    'error': {'color': 'red', 'bold': True}}


def success(self, message, *args, **kws):
    """Log 'msg % args' with severity 'SUCCESS' (level = 35).
    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.
    logger.success('Houston, we have a %s', 'thorny problem', exc_info=1)
    """
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = success


def initialize_logger_level(level):
    if level == 10:
        coloredlogs.install(level='DEBUG')
    elif level == 20:
        coloredlogs.install(level='INFO')
    elif level == 30:
        coloredlogs.install(level='WARNING')
    elif level == 40:
        coloredlogs.install(level='ERROR')
    elif level == 50:
        coloredlogs.install(level='CRITICAL')


def initialize_logger():
    logging.basicConfig(filename=PathManager.get_log_file_path(), format=LOG_FORMAT)
    initialize_logger_level(get_core_args().level)
