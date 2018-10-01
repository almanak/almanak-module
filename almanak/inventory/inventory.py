# Inventory methods
# Datamodels: structure, order

from typing import Dict

STATUS_CHOICES = ["ordered", "fetched",
                  "received", "finished", "returned", "missing"]


##############
# STRUCTURES #
##############
def get_structure(id: str):
    return True
    # return api.get(collection='storage_units', key=id)


def list_structures(filters: Dict):
    return True
    # return api.list(collection='storage_units', filters=filters)


def insert_structure(data: Dict):
    return True
    # return api.insert(collection='storage_units', data=data)


def update_structure(id: str, data: Dict):
    return True
    # return api.update(collection='storage_units', key=id, data=data)


def delete_structure(id: str):
    return True
    # return api.delete(collection='storage_units', key=id)


#########
# UNITS #
#########
def get_storage_unit(unit_id, projection=None):
    partition_key = {'unit_id', unit_id}
    unit = _get_item('storage_units', partition_key)
    return unit or {'error': True, 'msg': 'Unable to query local db.'}


def list_storage_units(user_id=None):
    kwargs = {}
    kwargs['table_name'] = 'storage_units'
    kwargs['pk'] = {'name': 'user_id', 'value': user_id}
    resp = _query_table(**kwargs)
    return resp


def insert_storage_unit(item):
    return False


def update_storage_unit(unit_id, status):
    return False


def delete_storage_unit(unit_id):
    return False


##########
# ORDERS #
##########
def get_order(user_id, resource_id):
    return _get_item('orders',
                     {'user_id': user_id},
                     {'resource_id': resource_id})


def list_orders(filters: Dict = None):
    return True
    # return api.list(collection='orders', filters=filters)


def list_orders(key, value, ids_only=False, limit=None):
    # List of orders only queries by partition_key, not also sort_key
    # as the sort_key of the orders-table is unique. Use _get_item for that
    kwargs = {}
    kwargs['table_name'] = 'orders'

    if key not in ['user_id', 'unit_id']:
        return {'error': True, 'msg': u'key must be unit_id or user_id'}

    kwargs['pk'] = {'name': key, 'value': value}
    if limit:
        kwargs['limit'] = limit

    if key == 'user_id':
        if ids_only:
            kwargs['proj'] = 'resource_id'
        return _query_table(**kwargs)
    else:
        kwargs['idx'] = 'unit_id-created-index'
        return _query_table(**kwargs)


def update_order():
    return True
    # return api.update(collection='orders', id=id, data=data)


def delete_order():
    return True
    # return api.delete(collection='orders', id=id)


def insert_order(user_id, resource_id, unit_id):
    """
    """
    # Fetch entities
    unit = get_storage_unit(unit_id)
    if unit.get('error'):
        return unit

    # Fetch user - need the email to send out confirmation
    user = get_user(user_id)
    if user.get('error'):
        return user

    existing_orders = list_orders(key='unit_id', value=unit_id)
    if isinstance(existing_orders, dict) and existing_orders.get('error'):
        return existing_orders

    # Test conditions
    # MOVE TO VIEW-HANDLER
    # if unit_id in user.get('active_units'):
    #     return {'msg': u'Du har allerede bestilt magasin-enheden'}

    # if len(user.get('active_units')) >= user.get('max_units'):
    #     return {'error': True, 'msg': u'Du kan ikke bestille flere materialer.'}

    # Baseline
    order = {
        'user_id': user_id,
        'resource_id': resource_id,
        'unit_id': unit_id
    }

    # If no existing orders on the unit
    if not existing_orders:
        # If unit is at readingroom, set status to available end expiration in 14 days
        if unit.get('status') == 'readingroom':
            order['status'] = 'available'
            order['expires'] = str(
                datetime.date.today() + datetime.timedelta(days=14))
            msg = u'Materialet er allerede tilgængelig på læsesalen.'
        # Else reserve the unit (like first in queue)
        else:
            order['status'] = 'waiting'
            msg = u'Materialet er bestilt. du får besked, når det er tilgængeligt på læsesalen.'
    # If existing orders on the unit, place in queue
    else:
        order['status'] = 'waiting'
        msg = unicode('Materialet er bestilt. Du er nummer ' +
                      str(len(existing_orders)) + ' i køen.')

    # Insert order
    if _put_item('orders', order):
        send_mail('order_created', user.get('email'))
        return {'msg': msg}
    else:
        return {'error': True, 'msg': 'Ukendt serverfejl. Bestillingen ikke gemt.'}

    # return api.insert(collection='orders', data=data)


def delete_order(user_id, resource_id):
    """Cancelled or finished or force-deleted by employee.
    """
    deleted_order = _delete_item('orders',
                                 {
                                     'user_id': user_id,
                                     'resource_id': resource_id
                                 },
                                 return_item=True)
    if not deleted_order:
        return {'error': True, 'msg': u'Kunne ikke slette ordren.'}

    # Fetch unit-status. If at readingroom, update next in line
    # and send availability-mail
    unit = get_storage_unit(deleted_order.get('unit_id'))
    if unit.get('status') == 'readingroom':
        # If next in line, update availability and expiration
        nxt = list_orders(
            key='unit_id', value=deleted_order.get('unit_id'), limit=1)
        if nxt:
            # Update order-keys and put back in db
            nxt[0]['status'] = 'available'
            nxt[0]['expires'] = str(
                datetime.date.today() + datetime.timedelta(days=14))
            if _put_item('orders', nxt[0], action='update'):
                # If order is updated, send availability-mail
                send_mail('order_available', nxt[0]['email'])

    return {'msg': u'Bestillingen er nu slettet.', 'id': resource_id}
