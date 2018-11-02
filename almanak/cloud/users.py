# Standard library
from os import environ as env

# Application libraries
from almanak.cloud._connectors import DynamoConnector


class UserService(DynamoConnector):
    def __init__(self):
        config = {
            'KEY_ID': env.get('ALMANAK_USER_KEY_ID'),
            'KEY': env.get('ALMANAK_USER_KEY'),
            'REGION': env.get('ALMANAK_USER_REGION'),
        }
        super().__init__(config)


    def get_user(self, user_id):
        return self._get('user', user_id)
