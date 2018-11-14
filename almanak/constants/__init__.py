# Constants as used by our webservices

# Resources identified by a persistent id, UUID4
PERSISTENT_RESOURCES = [
    "record",
    "person",
    "organisation",
    "event",
    "place",
    "location",
    "address",
    "collection",
    "object",
    "user",
    "structural_unit",
    "storage_unit",
    "client",
    "schema",
]

# Temporal resources identified by differing keys, eg. user_id, resource_id...
TEMPORAL_RESOURCES = ["bookmark", "search", "order", "autosuggestion", "searchdocument"]

# Query-filters (simple) for listing orders
ORDER_FILTERS = ["user_id", "client_id", "resource_id", "status"]

# Query-filters (simple) for listing structural_units
STRUCTURAL_UNIT_FILTERS = ["client_id", "path"]

# Possible locations for an archival_unit
UNIT_LOCATIONS = ["archive", "staged", "readingroom", "returned", "exported", "unknown"]

# Possible statuses for a given order
ORDER_STATUS = ["initialized", "available", "terminated"]

# Query-filters (complex) for listing records
RECORD_FILTERS = {
    "creators": {
        "label": "Ophavsretsholder",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "locations": {
        "label": "Stedsangivelse",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "events": {
        "label": "Begivenhed",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "people": {
        "label": "Person",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "organisations": {
        "label": "Organisation",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "collection": {
        "label": "Samling",
        "repeatable": False,
        "type": "object",
        "negatable": True,
    },
    "date_from": {
        "label": "Tidligste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False,
    },
    "date_to": {
        "label": "Seneste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False,
    },
    "subjects": {
        "label": "Emnekategori",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "series": {
        "label": "Arkivserie",
        "repeatable": False,
        "type": "string",
        "negatable": False,
    },
    "admin_tags": {
        "label": "Administrativt tag",
        "repeatable": True,
        "type": "string",
        "negatable": True,
    },
    "collection_tags": {
        "label": "Samlingstags",
        "repeatable": True,
        "type": "string",
        "negatable": True,
    },
    "content_types": {
        "label": "Materialetype",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "collectors": {
        "label": "Arkivskaber",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "curators": {
        "label": "Kurator",
        "repeatable": True,
        "type": "object",
        "negatable": True,
    },
    "availability": {
        "label": "Tilgængelighed",
        "repeatable": False,
        "type": "object",
        "negatable": True,
    },
    "usability": {
        "label": "Brugslicens",
        "repeatable": False,
        "type": "object",
        "negatable": True,
    },
    "registration_id": {
        "label": "RegistreringsID",
        "repeatable": False,
        "type": "integer",
        "negatable": False,
    },
}
