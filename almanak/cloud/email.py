# Standard library
import os

# Application libraries
from almanak.cloud._connectors import SESConnector as MailConnector


class EmailService(MailConnector):
    def send_mail(self, template, recipients, variables=None):
        return self._send(template, recipients)
