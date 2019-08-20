# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import ast
import logging
import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.api.errors import EmailError
from src.core.util.path_manager import PathManager
from src.core.api.os_helpers import OSHelper

from src.configuration.config_parser import get_config_property
from src.core.util.report_utils import Color

logger = logging.getLogger(__name__)


class EmailClient:

    def __init__(self):
        logger.info('Starting email reporting.')
        self.email_host = get_config_property('Email', 'smtp_ssl_host')
        self.email_port = get_config_property('Email', 'smtp_ssl_port')
        self.username = get_config_property('Email', 'username')
        self.password = get_config_property('Email', 'password')
        self.sender = get_config_property('Email', 'sender')
        self.targets = ast.literal_eval(get_config_property('Email', 'targets'))

    @staticmethod
    def create_email_subject(target):
        os_version = OSHelper.get_os_version().capitalize()
        date_today = date.today()
        email_info = '[{}][{}]Iris Test Report {}'.format('{} {}'.format(target.target_name, target.values['fx_version']) if target.target_name == 'Firefox' 
            else target.target_name, os_version, date_today)
        return email_info

    @staticmethod
    def get_file_attachment():
        test_report_file = os.path.join(PathManager.get_current_run_dir(), 'iris_log.log')
        if os.path.exists(test_report_file):
            file_log = open(test_report_file)
            attachment = MIMEText(file_log.read(), 1)
            file_log.close()
            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(test_report_file))
            return attachment
        else:
            raise Exception('File {} is not present in path'.format(test_report_file))

    def send_email_report(self, target: str, test_status: str, repo_details: str):
        email = MIMEMultipart()
        body_message = ""
        if isinstance(repo_details, dict):
            body_message = MIMEText((
                ' Repo_details:\n'
                ' Branch_name: {}\n'
                ' Branch_head: {}\n'
                ' Test_Run_Details: {}\n'
                ' Note: To see the complete run output, please check the attachment.'.format(
                    repo_details.get('iris_branch'), 
                    repo_details.get('iris_branch_head'), 
                    test_status)
                )) 
        else:
            raise EmailError("Invalid Body Message")


        email.attach(body_message)
        attachment = self.get_file_attachment()
        email.attach(attachment)

        email['From'] = self.sender
        email['To'] = ', '.join(self.targets)
        email['Subject'] = self.create_email_subject(target)

        server = smtplib.SMTP_SSL(self.email_host, self.email_port)

        try:
            server.login(self.username, self.password)
        except Exception:
            raise EmailError("User not logged into server. Please check your credentials.")
        else:
            logger.debug('User succesfully logged into email server')

            try:
                server.sendmail(self.sender, self.targets, email.as_string())
            except Exception:
                raise EmailError("Email was not sent. Please check for iris_log.log file.")
            else:
                server.quit()
                logger.info('Email successfully sent to {}'.format(self.targets))


def submit_email_report(target, result):

    """ PLACEHOLDER FOR EMAIL REPORT
        :param test_results: TEST RESULT SESSION
        need to update with appliications and git object
    """
    logger.info(' --------------------------------------------------------- '+Color.BLUE+'Starting Email report:'+Color.END+' ----------------------------------------------------------\n')
    email_report = EmailClient()
    email_report.send_email_report(target, str(result), PathManager.get_git_details())
