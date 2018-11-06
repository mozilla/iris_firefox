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

from iris.api.core.errors import EmailError
from iris.api.core.settings import get_os_version
from iris.api.core.util.core_helper import IrisCore
from iris.configuration.config_parser import get_config_property

logger = logging.getLogger(__name__)


class EmailClient:

    def __init__(self):
        logger.info('Starting email reporting.')
        self.email_host = get_config_property('EmailServerConfig', 'smtp_ssl_host')
        self.email_port = get_config_property('EmailServerConfig', 'smtp_ssl_port')
        self.username = get_config_property('EmailAccount', 'username')
        self.password = get_config_property('EmailAccount', 'password')
        self.sender = get_config_property('EmailRecipients', 'sender')
        self.targets = ast.literal_eval(get_config_property('EmailRecipients', 'targets'))

    @staticmethod
    def create_email_subject(firefox_version):
        email_info = '[Firefox %s][%s]Iris Test Report %s' % (
            firefox_version, get_os_version().capitalize(), date.today())
        return email_info

    @staticmethod
    def get_file_attachment():
        test_report_file = os.path.join(IrisCore.get_current_run_dir(), 'iris_log.log')
        if os.path.exists(test_report_file):
            file_log = open(test_report_file)
            attachment = MIMEText(file_log.read(), 1)
            file_log.close()
            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(test_report_file))
            return attachment
        else:
            raise Exception('File %s is not present in path' % test_report_file)

    def send_email_report(self, firefox_version, test_status, repo_details):
        email = MIMEMultipart()
        body_message = ""
        if isinstance(repo_details, dict):
            body_message = MIMEText(
                ''' Repo_details:\n ''' + """Branch_name:""" + repo_details.get(
                    'iris_branch')
                + " \n " + '''Branch_head: ''' + repo_details.get(
                    'iris_branch_head') + "\n\n" + '''Test_Run_Details: ''' + test_status +
                ''' \nNote: To see the complete run output, please check the attachment.''')
        else:
            raise EmailError("Invalid Body Message")

        email.attach(body_message)
        attachment = self.get_file_attachment()
        email.attach(attachment)

        email['From'] = self.sender
        email['To'] = ', '.join(self.targets)
        email['Subject'] = self.create_email_subject(firefox_version)

        server = smtplib.SMTP_SSL(self.email_host, self.email_port)

        try:
            server.login(self.username, self.password)
        except Exception:
            raise EmailError("User not logged into server. Please check your credentials.")
        else:
            try:
                server.sendmail(self.sender, self.targets, email.as_string())
            except Exception:
                raise EmailError("Email was not sent. Please check for iris_log.log file.")
            else:
                server.quit()
                logger.info('Email successfully sent to %s' % self.targets)
