# Standard library
from datetime import date, timedelta

# Application libraries
from almanak.cloud.constants import ORDER_STATUS, PERSISTENT_RESOURCES, TEMPORAL_RESOURCES
from almanak.cloud._connectors import DynamoConnector as conn


class InventoryService(conn):
    """Inherits base-methods from DynamoConnector
    Returns the dynamo-response directly - problem?
    """

    ##############
    # STRUCTURES #
    ##############

    # Structures are persistent resources
    def insert_structural_unit(self, data):
        """
        Args:

            data (dict): minimum keys: 'path', 'type', 'id'
                
        """
        return self._insert('structural_units', data)

    def get_structural_unit(self, uuid: str):
        """Id is a uuid4-string
        """
        return self._get('structural_units', uuid)
        
    def list_structural_units(self, key, value, ids_only=False, reverse=False, limit=None):
        """filters are often used to list structural_units under a given unit
        """
        data = {}
        data['_filter'] = {'key': key, 'value': value}
        data['limit'] = limit
        data['ids_only'] = ids_only
        data['reverse'] = reverse
        return self._list('structural_units', **data)

    def update_structural_unit(self, uuid: str, data):
        return self._update('structural_units', uuid, data)

    def delete_structural_unit(self, uuid: str):
        return self._delete('structural_units', uuid)

    #########
    # UNITS #
    #########

    # Units are persistent resources
    def insert_storage_unit(self, data):
        """data is a dict with a minimum of keys: ...
        These keys can change without the function having to change. All
        that is required are the required keys
        """
        return self._insert('storage_units', data)

    def get_storage_unit(self, uuid: str):
        """Id is a uuid4-string
        """
        return self._get('storage_units', uuid)

    def list_storage_units(self, key, value, ids_only=False, reverse=False, limit=None):
        """Maybe also use for listing which storage_units are placed in
        a given structural_unit
        """
        data = {}
        data['_filter'] = {'key': key, 'value': value}
        data['limit'] = limit
        data['ids_only'] = ids_only
        data['reverse'] = reverse
        return self._list('storage_units', **data)

    def update_storage_unit(self, uuid: str, data):
        return self._update('storage_units', uuid, data)

    def delete_storage_unit(self, uuid: str):
        return self._delete('storage_units', uuid)

    ##########
    # ORDERS #
    ##########

    # Orders are temporal resources.
    # Id is a dict. A combination of user_id and resource_id
    def insert_order(self, user_id: str, resource_id: str, unit_id: str):
        """ """
        order = {
            'user_id': user_id,
            'resource_id': resource_id,
            'storage_unit': unit_id
        }

        current_orders = self._list('orders', {'unit_id': unit_id})
        if current_orders.get('error'):
            order['status'] = 'initialized'
            msg = 'Materialet er bestilt.'
        elif current_orders.get('data') is None:
            unit = self._get('storage_units', unit_id)
            if unit.get('error'):
                order['status'] = 'initialized'
                msg = 'Materialet er bestilt.'
            elif unit.get('location') == 'readingroom':
                order['status'] = 'available'
                order['expires'] = str(date.today() + timedelta(days=14))
                msg = 'Materialet er tilgængelig på læsesalen.'
        else:
            order['status'] = 'initialized'
            msg = 'Du er nummer ' + str(len(current_orders.get('data'))) + ' i køen.'

        result = self._insert('orders', order)
        if result.get('error'):
            return result
        else:
            from ._connectors import SESConnector
            mail = SESConnector()
            mail._send('order_created', user_id, msg)
            return {'msg': msg}

    def list_orders(self, key, value, ids_only=False, reverse=False, limit=None):
        # List of orders only queries by partition_key, not also sort_key
        # as the sort_key of the orders-table is unique. Use _get_item for that
        data = {}
        data['_filter'] = {'key': key, 'value': value}
        data['limit'] = limit
        data['ids_only'] = ids_only
        data['reverse'] = reverse
        return self._list('orders', **data)

    def get_order(self, user_id: str, resource_id: str):
        """ """
        _id = {'user_id': user_id, 'resource_id': resource_id}
        return self._get('orders', _id)

    def update_order(self, user_id: str, resource_id: str, status: str):
        """Complex. Needs to check the status and any reservations all the time"""
        _id = {'user_id': user_id, 'resource_id': resource_id}
        data = {'status': status}
        return self._update('orders', _id, data)

    def delete_order(self, user_id: str, resource_id: str):
        """Cancelled or finished or force-deleted by employee.
        """
        _id = {'user_id': user_id, 'resource_id': resource_id}

        # delete order
        order = self._delete('orders', _id, return_item=True)        
        if order.get('error'):
            return order

        # get unit-info in relation to deleted order
        unit = self._get('storage_units', order.get('unit_id'))
        if unit.get('error'):
            # TODO: What happens when the unit is not fetched?
            return unit

        # get reservations on the unit
        queue = self._list(
            'orders',
            {'unit_id': unit.get('unit_id')},
            limit=1
        )
        if queue.get('error'):
            # TODO: What happens when the first reservation is not notified?
            return queue

        # if the storage_unit has reserved resources and unit-location is readingroom
        # then update next order with status 'available' and send mail
        if queue and unit.get('status') == 'readingroom':
            first = queue[0]
            # Update order-keys and put back in db
            first['status'] = 'available'
            first['expires'] = str(date.today() + timedelta(days=14))

            # If order is updated, send availability-mail
            _id = {
                'user_id': first.get('user_id'),
                'resource_id': first.get('resource_id')
            }
            result = self._update('orders', _id, first)
            if result.get('error'):
                send_mail('order_available', nxt[0]['email'])

        return {'msg': u'Bestillingen er nu slettet.', 'id': resource_id}
