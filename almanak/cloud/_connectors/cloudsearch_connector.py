# Standard library
from os import environ as env

# Third party
from boto3 import client


class CloudsearchConnector:
    """Search: CRUD
    """
    def __init__(self):
        self.db = client(
            'cloudsearchdomain',
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            region_name=env.get("AWS_REGION_NAME"),
            endpoint_url=env.get("AWS_CLOUDSEARCH_ENDPOINT")
        )

    