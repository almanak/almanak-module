# -*- coding: UTF-8 -*-
from os import environ as env

# Third party
import boto3
from botocore.exceptions import ClientError


class SESConnector:
    def __init__(self, config):
        self.conn = boto3.client(
            "ses",
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            region_name=env.get("AWS_EMAIL_REGION_NAME"),
        )

    # Mail-templates
    TEMPLATES = {
        "order_available": {
            "subject": "Din ordre er nu tilgængelig på læsesalen",
            "body": "Body for order_available",
            "html": "<head></head><body>order_available</body>",
        },
        "order_expiring": {
            "subject": "Din bestilling udløber om en uge",
            "body": "Body for order_expiring",
            "html": "<head></head><body>order_expiring</body>",
        },
        "unit_exported": {
            "subject": "Bestilling(er) forsinket.",
            "body": "Body for unit_exported",
            "html": "<head></head><body>unit_exported</body>",
        },
    }

    # Try to send the email.
    def _send(self, template, recipients):
        temp = self.TEMPLATES.get(template)
        try:
            # Provide the contents of the email.
            api_response = self.conn.send_email(
                Destination={"ToAddresses": recipients},
                Message={
                    "Body": {
                        "Html": {"Charset": "UTF-8", "Data": temp.get("html")},
                        "Text": {"Charset": "UTF-8", "Data": temp.get("body")},
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        # 'Data': temp.get('subject'),
                        "Data": temp.get("subject"),
                    },
                },
                Source="AarhusArkivet <cjk@aarhus.dk>",
            )
            return {"status": api_response.get("msg", "no msg-key in response")}

        except Exception as e:
            return {"error": e}  # api_response['Error']['Message']
