# Standard library
from os import environ as env
from datetime import date, timedelta

# Application library-stuff
from almanak.constants import ORDER_STATUS, PERSISTENT_RESOURCES, TEMPORAL_RESOURCES
from almanak._helpers import response_handler
from almanak.cloud._connectors import DatastoreConnector

# Application services
from almanak.cloud import EmailService
from almanak.cloud import UserService


class InventoryService(DatastoreConnector):
    """Inherits base http-methods from DatastoreConnector
    """

    def __init__(self, config):
        # self.mail_service = MailService()
        self.user_service = UserService()
        super().__init__(config)

    ##############
    # STRUCTURES #
    ##############
    def insert_structural_unit(self, data, username):
        """Insert a structural unit

        Args:
            data (dict):
                id (str): barcode, label or other
                label (str): possible label, eg. "Reol 32"
                type (str): freeform type, eg. "shelf" or "drawer"
                location (str): hierarchical location-string, eg.
                    "Vester Alle 12/Magasin 001"
                path_label (str): hierarchical unit_path, eg.
                    "Reol 11/Fag 4"
                path (list): list of uuid's of all parent structural_units, eg.
                    ["339d0933-d5c6-4e48-9c3b-c8ff0faed824", "132d0933-d5c6-4e48-9c3b-c8ff0faed843"]
            username (str): the user doing the insertion
        Returns:   
            dict with 'status', plus 'data' or 'error'
        """
        # out = []
        # for i, s in enumerate(data.get('path').split('/')):
        #     if i == 0:
        #         out.append(s)
        #     else:
        #         out.append('/'.join([out[i-1], s]))
        # data['path'] = out

        # path_str = data.get('path')
        # path_list = []
        # start = 1
        # while start > 0:
        #     idx = path_str.find('/', start)
        #     if idx > -1:
        #         path_list.append(path_str[0:idx+1])
        #     elif start == 1:
        #         path_list.append(path_str)
        #     start = idx
        # data['path'] = [path_str]

        resp = self._insert("structural_unit", data, username=username)
        return response_handler(resp)

    def get_structural_unit(self, uuid):
        """Get a structural unit (shelf, drawer, rack...)

        Args:
            uuid (str): uuid of the structural unit (required)
        
        Returns:
            The structural unit in a 'data'-key or an 'error'-key
        """
        resp = self._get("structural_unit", uuid)
        return response_handler(resp)

    def list_structural_units(self, path=[]):
        """List all structural units of a given client

        Args:
            path (list): list of uuid's of parent_units to filter by

        Returns:
            List of structural units in a 'data'-key
        """
        filters = [("path", "=", uuid) for uuid in path] if path else None
        resp = self._list("structural_unit", filters=filters)
        return response_handler(resp)

    def update_structural_unit(self, uuid, data, username):
        resp = self._update("structural_unit", uuid, data, username=username)
        return response_handler(resp)

    def delete_structural_unit(self, uuid, username):
        resp = self._delete("structural_unit", uuid, username=username)
        return response_handler(resp)

    #########
    # UNITS #
    #########
    def insert_storage_unit(self, data, username):
        """Insert a storage_unit

        Args:
            data (dict):
                id (str): barcode, unit_id, eg. '91+000923-1'
                type (str): freeform type, eg. "box" or "protokol"
                current_location (str): archive, readingroom, in transit...
                structural_unit_id (str): uuid of the closest structural_unit
            username (str): username

        Returns:   
            dict with 'status', plus 'data' or 'error'
        """
        resp = self._insert("storage_unit", data, username=username)
        return response_handler(resp)

    def get_storage_unit(self, uuid):
        """Id is a uuid4-string
        """
        resp = self._get("storage_unit", uuid)
        return response_handler(resp)

    def list_storage_units(self, structural_unit_id=None, ids_only=False):
        """Maybe use for listing which storage_units are placed in
        a given structural unit.
        """
        if structural_unit_id:
            filters = [("structural_unit_id", "=", structural_unit_id)]
        else:
            filters = None
        resp = self._list("storage_unit", filters=filters, ids_only=ids_only)
        return response_handler(resp)

    def update_storage_unit(self, uuid, data, username):
        resp = self._update("storage_unit", uuid, data, username=username)
        return response_handler(resp)

    def update_storage_unit_location(self, uuid, location, username):
        """If the location is readingroom, this triggers mail(s)
        """
        data = {"current_location": location}
        update = self._update("storage_unit", uuid, data, username=username)
        if update.get("error"):
            # log this
            return {"error": "unable to update location of storage_unit"}

        if location == "readingroom":
            order = self._list("order", filters=[("storage_unit", "=", uuid)], limit=1)
            if order.get("error"):
                # log this!
                return {"error": "unable to fetch order related to storage_unit"}

            if order.get("data"):
                user_id = order["data"].get("user_id")
                user = self.user_service.get_user(user_id)
                if user.get("error"):
                    # log this
                    return {"error": "unable to fetch user to send mail"}

                # email = user["data"].get("email")
                # sent_mail = self.mail_service.send_mail("order_available", [email])
                # if sent_mail.get("error"):
                #     # log this
                #     return {"error": "unable to send mail to user"}

                return {"status": 200, "msg": "Location of unit updated. Mail sent."}

            return {"status": 200, "msg": "Location of unit updated"}
        else:
            return {"status": 200, "msg": "Location of unit updated"}

    def delete_storage_unit(self, uuid, username):
        resp = self._delete("storage_unit", uuid, username=username)
        return response_handler(resp)

    ##########
    # ORDERS #
    ##########
    def insert_order(self, data, username):
        """Inserts an order on a given resource situated in a certain
        storage_unit.

        Args:
            data (dict):
                resource_id (str): identifier of the requested resource
                storage_unit_id (str): id (not uuid) of the storage_unit
                user_id (str): uuid or sub_id of the user
            username (str): name of the user requesting the order
        """
        resource_id = data.get("resource_id")
        storage_unit_id = data.get("storage_unit_id")
        user_id = data.get("user_id")

        # Current orders
        resp = self._list("order", filters=[("storage_unit_id", "=", storage_unit_id)])

        # If the existing order-call fails, return
        if resp.get("error"):
            return {"error": resp.get("error")}

        # setup order
        order = {
            "resource_id": resource_id,
            "storage_unit_id": storage_unit_id,
            "user_id": user_id,
            "username": username,
        }

        # Return if user already ordered from the same storage_unit,
        # else assign order-vars with queue-info
        orders = resp.get("data")
        if orders:
            if user_id in [e.get("user_id") for e in orders]:
                return {"error": "User already has an order from the same unit"}
            else:
                order["status"] = "initialized"
                msg = "Du er nummer " + str(len(orders)) + " i køen."
        else:
            resp = self._get("storage_unit", storage_unit_id)
            if resp.get("error"):
                return {"error": "unable to fetch related storage_unit-info"}

            # If unit is fetched and currently at the readingroom
            unit = resp.get("data")
            if unit and (unit.get("current_location") == "readingroom"):
                order["status"] = "available"
                order["expires"] = str(date.today() + timedelta(days=14))
                msg = "Materialet er tilgængelig på læsesalen."
            # else just initialize the order
            else:
                order["status"] = "initialized"
                msg = "Materialet er bestilt."

        # Insert order
        resp = self._insert("order", order, order.get("username"))
        if not resp.get("error"):
            # send mail to user
            resp["msg"] = msg
        return resp

    def get_order(self, uuid):
        """ """
        resp = self._get("order", uuid)
        return response_handler(resp)

    def list_orders(self, user_id=None, storage_unit_id=None, status=None):
        filters = []
        if user_id:
            filters.append(("user_id", "=", user_id))
        if storage_unit_id:
            filters.append(("storage_unit_id", "=", storage_unit_id))
        if status:
            filters.append(("status", "=", status))

        resp = self._list("order", filters=filters)
        return response_handler(resp)

    def update_order(self, uuid, username):
        """Currently this only activates an order
        """
        data = {"status": "activated"}
        resp = self._update("order", uuid, data, username=username)

        if resp.get("error"):
            return resp

        # TODO - send mail, that order is available.
        return {"status": 200, "msg": "Order activated. User notified."}

    def delete_order(self, uuid, username):
        """Cancelled or finished or force-deleted (by employee).

        What happends when any of the calls after the delete_order-call fails?
        """
        deleted_order = self._delete("order", uuid, username, return_entity=True)
        if deleted_order.get("error"):
            return deleted_order

        # Get unit in relation to deleted order, or return
        unit_id = deleted_order["data"].get("storage_unit_id")
        unit = self._get("storage_unit", unit_id)
        if unit.get("error"):
            return {"msg": "Order deleted, but unable to fetch unit-location."}

        # If unit at readingroom...
        if unit["data"].get("current_location") == "readingroom":
            # and one or more reservations on the unit
            queue = self._list("order", filters=[("storage_unit_id", "=", unit_id)])
            # Get queue or return
            if queue.get("error"):
                return {"error": "Order deleted, but unable to fetch queue-info."}

            if queue.get("data"):
                order = queue["data"][0]
                order["status"] = "available"
                order["expires"] = str(date.today() + timedelta(days=14))
                update = self._update("order", order.get("uuid"), order, username)
                if update.get("error"):
                    return {
                        "error": "Order deleted, but unable to update next-in-line."
                    }
                return {"msg": "Order deleted. Next-in-line updated"}
                # send mail with order-available msg to nxt.get('user_id')
                # if we come this far and send_mail fails, it must be logged!!
                # otherwise the user will never be told, that the order is ready
        return {"msg": "Order deleted."}

