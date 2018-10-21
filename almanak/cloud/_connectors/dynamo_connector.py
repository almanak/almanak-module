# Standard library
from os import environ as env
from datetime import datetime

# Third party
from boto3 import resource
from boto3.dynamodb.conditions import Key  # , Attr


class DynamoConnector():
    """Users: bookmarks, saved_searches, preferences, CRUD
    Inventory: Storage_units, structures and orders, CRUD
    """
    def __init__(self):
        self.db = resource(
            'dynamodb',
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            region_name=env.get("AWS_REGION_NAME")
        )

    def _response_handler(self, table, method, data):
        table = self.db.Table(table)
        try:
            if method == 'get':
                resp = table.get_item(**data)
            elif method == 'list':
                resp = table.query(**data)
            elif method == 'insert':
                resp = table.put_item(Item=data)
            elif method == 'replace':
                resp = table.put_item(Item=data)
            elif method == 'update':
                resp = table.get_item(**data)

            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                if method in ['insert', 'replace', 'update']:
                    return resp.get('Item')
                elif method == 'list':
                    return resp.get('Items')
                else:
                    return resp
            else:
                return {'error': resp}
        except Exception as e:
            # log.exception(e)
            return {'error': e}


    ################
    # BASE METHODS #
    ################
    def _get(self, table, _id):
        """_id is a uuid-string or adict with minimum a primary key,
        and possibly sort_key, eg:
        {'user_id': <user_id>, 'resource_id': <resource_id>}
        """
        data = {'Key': _id}
        return self._response_handler(table, 'get_item', data)

    def _insert(self, table, data):
        """
        Add one item to table. data is a dictionary {col_name: value}.
        """
        now = datetime.utcnow().isoformat()
        data['created'] = now
        data['updated'] = now
        return self._response_handler(table, 'put_item', data)

    def _replace(self, table, data):
        """
        Replace one item to table. data is a dictionary {col_name: value}.
        """
        data['updated'] = datetime.utcnow().isoformat()
        return self._response_handler(table, 'put_item', data)

    def _update(self, table, _id, update_field):
        """
        table: name of the table
        _id: uuid-string or dict containing the key name and val
        update_field: dict containing the key name and value of the
        attribute to be updated
        eg. {"attribute": "processing_status", "value": "completed"}
        """
        table = self.db.Table(table)
        update_expr = 'SET updated=:now, {}=:val1'.format(update_field['attribute'])

        response = table.update_item(
            Key=_id,
            UpdateExpression=update_expr,
            ExpressionAttributeValues={
                ':now': datetime.utcnow().isoformat(),
                ':val1': update_field['value']
            },
            ReturnValues='ALL_NEW'
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return response.get('Attributes')
        else:
            return False

    def _delete(self, table, _id, return_item=False):
        """Delete _id from resource.
        _id can be a string or dict consisting of partition-key and
        possibly a sort_key, all in _id-dict
        """
        data = {
            'Key': _id,
            'ReturnValues': 'ALL_OLD' if return_item else 'NONE'
        }

        return self._response_handler(table, 'delete_item', data)

    def _list(self, table, _filter=None, idx=None, reverse=None, ids_only=None, limit=None):
        """
        Perform a query operation on the table.
        """
        data = {}
        if _filter:
            data['KeyConditionExpression'] = Key(_filter.get('key')).eq(_filter.get('value'))

        if ids_only:
            data['ProjectionExpression'] = 'resource_id'

        if idx:
            data['IndexName'] = idx

        if limit:
            data['Limit'] = limit

        # reverse_direction. Used when sorting descending
        if reverse:
            data['ScanIndexForward'] = False

        return self._response_handler(table, 'list', data)

    # def __scan_table(self, table, filter_key=None, filter_value=None, limit=None):
    #     """
    #     Perform a scan operation on table. Can specify filter_key (col name) and its value to be filtered. This gets all pages of results.
    #     Returns list of items.
    #     http://boto3.readthedocs.io/en/latest/reference/customizations/dynamodb.html#dynamodb-conditions
    #     """
    #     table = self.db.Table(table)
    #     kwargs = {}

    #     if filter_key and filter_value:
    #         kwargs['FilterExpression'] = Key(filter_key).eq(filter_value)
    #     kwargs['Limit'] = limit or None
    #     # response = table.scan(FilterExpression=filtering_exp)
    #     response = table.scan(**kwargs)

    #     items = response['Items']
    #     while True:
    #         if response.get('LastEvaluatedKey'):
    #             response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    #             items += response['Items']
    #         else:
    #             break

    #     return items
