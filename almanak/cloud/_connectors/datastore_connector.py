# Standard library
from os import environ as env
from datetime import datetime
from uuid import uuid1, uuid4

# Third party
from google.cloud import datastore

# Application libraries
from almanak.constants import PERSISTENT_RESOURCES, TEMPORAL_RESOURCES


class DatastoreConnector:
    """Inventory and later: Entities, Autosuggest, Records, Assets
    """
    def __init__(self, config):
        self.db = datastore.Client.from_service_account_json(config)

    def _insert(self, resource, data, username):
        """Insert an entity into a resource (datastore-Kind)

        Args:
            resource (str): the resource
            data (dict): the resource-specific properties
            username (str): label for the user doing the updating
        
        Returns:
            dict: status (int), plus 'error' (str) or 'data' (list)
        """
        return self._multi_insert(resource, [data], username)

        # now = datetime.utcnow().isoformat()

        # data["client_id"] = int(env.get("ALMANAK_CLIENT_ID"))
        # data["created"] = now
        # data["created_by"] = username
        # data["updated"] = now
        # data["updated_by"] = username

        # # Use uuid4 for persistent resources, else use timestamp
        # if resource in PERSISTENT_RESOURCES:
        #     uuid = str(uuid4())
        # elif resource in TEMPORAL_RESOURCES:
        #     uuid = str(uuid1())
        # else:
        #     raise ValueError("No such resource: " + resource)

        # # set the uuid as the key and its own property
        # data["uuid"] = uuid
        # key = self.db.key(resource, uuid)
        # # Initialize and populate
        # entity = datastore.Entity(key=key)
        # entity.update(data)
        # try:
        #     self.db.put(entity)
        #     return {"status": 201, "data": dict(entity)}
        # except ValueError as e:
        #     return {"error": str(e)}

    def _multi_insert(self, resource, datalist, username):
        """Insert an entity into a resource (datastore-Kind)

        Args:
            resource (str): the name of the resource
            datalist (list): list of the resources
            username (str): label for the user doing the updating
        
        Returns:
            dict: status (int), plus 'error' (str) or 'data' (list)
        """
        if len(datalist) > 25:
            raise ValueError("Max allowed entities per batch is 25")
        
        entities = []

        for data in datalist:
            now = datetime.utcnow().isoformat()

            data["client_id"] = int(env.get("ALMANAK_CLIENT_ID"))
            data["created"] = now
            data["created_by"] = username
            data["updated"] = now
            data["updated_by"] = username

            # Use uuid4 for persistent resources, else use timestamp
            if resource in PERSISTENT_RESOURCES:
                uuid = str(uuid4())
            elif resource in TEMPORAL_RESOURCES:
                uuid = str(uuid1())
            else:
                raise ValueError("No such resource: " + resource)

            # set the uuid as the key and its own property
            data["uuid"] = uuid
            key = self.db.key(resource, uuid)
            # Initialize and populate
            entity = datastore.Entity(key=key)
            entity.update(data)
            entities.append(entity)

        try:
            self.db.put_multi(entities)
            return {"status": 201, "data": [dict(e) for e in entities]}
        except ValueError as e:
            return {"status": 400, "error": str(e)}

    def _get(self, resource, uuid):
        """Get en entity from a resource
        """
        _key = self.db.key(resource, uuid)
        try:
            entity = self.db.get(_key)
            if entity:
                return {"status": 200, "data": dict(entity)}
            else:
                return {"status": 404, "error": "No such entity"}
        except ValueError as e:
            return {"status": 400, "error": str(e)}

    def _list(
        self, resource, filters=[], projection=[], sort=[], limit=None, ids_only=False
    ):
        """Fetches list of resources.

        Args:
            resource (str): the resourcetype to list, eg. 'events', 'records',
                'storage_units', 'orders', 'users'...
            filters (list): tuplelist of resource-relevant property-filters, eg.
                [ ('name', '=', 'eva'), ('age', '>' , '5') ] 
            projection (list): ['address', 'name']
            sort (list): use '-' to order desc, eg. ['created', '-priority']

        Returns:
            List of resources matching the supplied filters, if any.
        """

        query = self.db.query(kind=resource)
        if filters:
            for tup in filters:
                query.add_filter(*tup)
        if projection:
            query.projection = projection
        if sort:
            query.order = sort
        # I'm using uuid as keys, as keys_only() returns Entity Keys
        if ids_only:
            query.projection = ["uuid"]
        try:
            res = query.fetch(limit=limit)
            return {"status": 200, "data": [dict(i) for i in res] if res else []}
        except Exception as e:
            return {"error": str(e)}

    def _update(self, resource, uuid, data, username):
        try:
            entity = self.db.get(self.db.key(resource, uuid))
        except ValueError as e:
            return {"error": str(e)}

        data["updated"] = datetime.utcnow().isoformat()
        data["updated_by"] = username
        entity.update(data)

        try:
            self.db.put(entity)
            return {"status": 200, "data": dict(entity)}
        except ValueError as e:
            return {"error": str(e)}

    def _delete(self, resource, uuid, username, return_entity=False):
        if return_entity:
            try:
                resp = self.db.get(self.db.key(resource, uuid))
            except ValueError as e:
                return {"errror": str(e)}

            self.db.delete(self.db.key(resource, uuid))
            return {"status": 204, "data": dict(resp)}
        else:
            self.db.delete(self.db.key(resource, uuid))
            return {"status": 204, "msg": "Entity deleted"}
