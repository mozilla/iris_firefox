# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from iris.api.core.util.core_helper import *
from iris.configuration.config_parser import *
import ast
from datetime import date
from iris.api.core.settings import *

logger = logging.getLogger(__name__)


class EmailClient:

    def __init__(self):
        logger.info('Starting Email reporting.')

        self.email_host = get_credential('EmailServerConfig', 'smtp_ssl_host')
        self.email_port = get_credential('EmailServerConfig', 'smtp_ssl_port')
        self.username = get_credential('EmailAccount', 'username')
        self.password = get_credential('EmailAccount', 'password')
        self.sender = get_credential('EmailRecipients', 'sender')
        self.targets = ast.literal_eval(get_credential('EmailRecipients', 'targets'))

    @staticmethod
    def create_email_subject(firefox_version):
        email_info = '[Firefox %s][%s]Iris Test Report %s' % (
            firefox_version, Settings.get_os().capitalize(), date.today())
        return email_info

    @staticmethod
    def get_file_attachment():

        test_run_report_dir = get_current_run_dir()

        test_report_file = os.path.join(test_run_report_dir,
                                        'iris_log.log')
        if test_report_file is not None:
            file_log = open(test_report_file)
            attachment = MIMEText(file_log.read(), 1)
            file_log.close()

            attachment.add_header('Content-Disposition',
                                  'attachment',
                                  filename=os.path.basename(test_report_file))

            return attachment
        else:
            raise Exception('File %s is not present in path' % test_report_file)

    def send_email_report(self, firefox_version):
        email = MIMEMultipart()
        body_message = MIMEText(''' Iris Email Report.
                                       \nNote: To see the complete test stacktrace please check the attachment.''')
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
            raise EmailError("User not logged into server,please check your credentials.")
        else:
            try:
                server.sendmail(self.sender, self.targets, email.as_string())
            except Exception:
                raise EmailError("Email was not sent,please check if iris_log.log file .")
            else:
                server.quit()
                logger.info('Email successfully sent to %s' % self.targets)
