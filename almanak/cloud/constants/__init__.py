# Constants as used by our webservices

# Resources identified by a persistent id, UUID4
PERSISTENT_RESOURCES = [
    "records",
    "people",
    "organisations",
    "events",
    "places",
    "locations",
    "addresses",
    "collections",
    "objects",
    "users",
    "structural_units",
    "storage_units",
    "clients",
    "schemas",
]

# Temporal resources identified by differing keys, eg. user_id, resource_id...
TEMPORAL_RESOURCES = [
    "bookmarks",
    "searches",
    "orders",
    "autosuggestions",
    "searchdocuments",
]

# Query-filters (simple) for listing orders
ORDER_FILTERS = [
    "user_id",
    "client_id",
    "resource_id",
    "status",
]

# Query-filters (simple) for listing structural_units
STRUCTURAL_UNIT_FILTERS = [
    "client_id",
    "path",
]

# Query-filters (complex) for listing records
RECORD_FILTERS = {
    'creators': {
        "label": u"Ophavsretsholder",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'locations': {
        "label": u"Stedsangivelse",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'events': {
        "label": u"Begivenhed",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'people': {
        "label": u"Person",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'organisations': {
        "label": u"Organisation",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'collection': {
        "label": u"Samling",
        "repeatable": False,
        "type": "object",
        "negatable": True
    },
    'date_from': {
        "label": u"Tidligste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False
    },
    'date_to': {
        "label": u"Seneste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False
    },
    'subjects': {
        "label": u"Emnekategori",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'series': {
        "label": u"Arkivserie",
        "repeatable": False,
        "type": "string",
        "negatable": False
    },
    'admin_tags': {
        "label": u"Administrativt tag",
        "repeatable": True,
        "type": "string",
        "negatable": True
    },
    'collection_tags': {
        "label": u"Samlingstags",
        "repeatable": True,
        "type": "string",
        "negatable": True
    },
    'content_types': {
        "label": u"Materialetype",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'collectors': {
        "label": u"Arkivskaber",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'curators': {
        "label": u"Kurator",
        "repeatable": True,
        "type": "object",
        "negatable": True
    },
    'availability': {
        "label": u"Tilgængelighed",
        "repeatable": False,
        "type": "object",
        "negatable": True
    },
    'usability': {
        "label": u"Brugslicens",
        "repeatable": False,
        "type": "object",
        "negatable": True
    },
    'registration_id': {
        'label': u'RegistreringsID',
        'repeatable': False,
        'type': 'integer',
        'negatable': False
    }
}

# Possible locations for an archival_unit
UNIT_LOCATIONS = [
    "archive",
    "readingroom",
    "exported",
    "transit",
    "unknown",
]

# Possible statuses for a given order
ORDER_STATUS = [
    "initialized",
    "available",
    "terminated",
]
