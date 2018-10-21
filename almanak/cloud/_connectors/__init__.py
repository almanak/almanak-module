from almanak.cloud._connectors.dynamo_connector import DynamoConnector
from almanak.cloud._connectors.cloudsearch_connector import CloudsearchConnector
from almanak.cloud._connectors.ses_connector import SESConnector
from almanak.cloud._connectors.datastore_connector import DatastoreConnector

# All persistent-connectors must implement all or some of the following
# interface:

# _get_resource(collection: str, id: str)
# _insert_resource(collection: str, id: str)
# _list_resources(collection: str, filters: Dict = None)
# _update_resource(collection: str, id: str, data: Dict)
# _delete_resource(collection: str, id: str)

# In addition, upsert(), scan_resources() and batch_methods might be
# implemented.

# Other connectors can implement whatever, eg, autosuggest

# They must also implement unified error-handling. How??
