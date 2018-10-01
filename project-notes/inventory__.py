#!/usr/bin/env python

import webapp2
import logging
import json
import datetime
from google.appengine.ext import ndb

STATUS_CHOICES = ["ordered", "fetched", "received", "finished", "returned", "missing"]


class Order(ndb.Model):
    """List of active orders"""
    createdAt = ndb.DateTimeProperty(auto_now_add=True)
    updatedAt = ndb.DateTimeProperty(auto_now=True)
    client = ndb.StringProperty(required=True, choices=VALID_CLIENTS)
    barcode = ndb.StringProperty(required=True)
    structuralBarcode = ndb.StringProperty(required=True)
    status = ndb.StringProperty(required=True, choices=STATUS_CHOICES)
    username = ndb.StringProperty(required=True)
    userID = ndb.StringProperty(required=True, indexed=True)


class Structure(ndb.Model):
    """Structure for a given archival space"""
    createdAt = ndb.DateTimeProperty(auto_now_add=True)
    updatedAt = ndb.DateTimeProperty(auto_now=True)
    client = ndb.StringProperty(required=True, choices=VALID_CLIENTS)
    label = ndb.StringProperty(required=True)
    structure = ndb.JsonProperty(required=True)


class JsonHandler(webapp2.RequestHandler):
    def handle_exception(self, exception, debug_mode):
        logging.exception(exception)
        error = {}
        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
            self.render({"error": exception.title})
        else:
            self.response.set_status(500)
            self.render({"error": "Unspecified server-error."})

    def valid_request(self):
        req = self.request
        if not req.headers.get('x-almanak-client-id', None) in VALID_CLIENTS:
            self.abort(400, title='Missing or invalid client-id')
        if not req.headers.get('x-almanak-application-id', None) in VALID_APPLICATIONS:
            self.abort(400, title='Missing or invalid application-id')

        if req.method in ['POST', 'PUT']:
            if not req.body:
                self.abort(400, title='Missing body from POST-request')

            if 'application/json' not in req.content_type:
                self.abort(400, title="The API only supports requests encoded as JSON")

            try:
                temp = json.loads(req.body.decode('utf-8'))
            except (ValueError, UnicodeDecodeError, TypeError):
                self.abort(400, title='Could not decode the request body. The '
                                                    'JSON was incorrect or not encoded as '
                                                    'UTF-8.')
        return True

    def render(self, obj):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(obj))


class InventoryListHandler(JsonHandler):

    def post(self):
        """Add an order to an institution's orderlist"""
        if self.valid_request():
            order = json.loads(self.request.body.decode('utf-8'))

            if not order.get('userID'):
                self.abort(400, title='Required user-id missing')
            if not order.get('username'):
                self.abort(400, title='Missing username')
            if not order.get('barcode'):
                self.abort(400, title='Missing barcode')
            if not len(order.get('barcode')) == 10 or (order.get('barcode')[-1] != '1'):
                self.abort(400, title='Malformed barcode')
            if not order.get('structuralBarcode'):
                self.abort(400, title='Missing shelf_barcode')
            if not len(order.get('structuralBarcode')) == 10 or (order.get('structuralBarcode')[-1] != '2'):
                self.abort(400, title='Malformed shelf_barcode')

            new_order = Order()
            new_order.client = self.request.headers.get('x-almanak-client-id')
            new_order.username = order.get('username')
            new_order.userID = order.get('userID')
            new_order.barcode = order.get('barcode')
            new_order.structuralBarcode = order.get('structuralBarcode')
            new_order.status = "ordered"
            new_order.key = ndb.Key(Order, order.get('barcode'))
            order_key = new_order.put()

            self.response.set_status(201)
            self.response.headers["Location"] = ('/').join([BASE_URL, 'orders', str(order_key.id())])
            self.render({"message": "OrdreID: " + order.get('barcode') + " oprettet"})


class InventoryItemHandler(JsonHandler):
    def get(self, order_id):
        """Fetch a single order"""
        if self.valid_request():
            order = Order.get_by_id(order_id)
            if order and order.client == self.request.headers.get('x-almanak-client-id'):
                self.render(_make_serializable(order))
            else:
                self.abort(404, title="No current order")

    def put(self, order_id):
        """Update the 'status' of a single order"""
        if self.valid_request():
            order = Order.get_by_id(order_id)

            if order and order.client == self.request.headers.get('x-almanak-client-id'):
                request = json.loads(self.request.body.decode('utf-8'))
                status = request.get('status')

                if status not in STATUS_CHOICES:
                    self.abort(400, title='Invalid status-value')

                order.status = status
                order.put()
                self.render({"message": "Ordre nr. " + order_id + " opdateret"})
            else:
                self.abort(404, title="No existing order with that ID")

    def delete(self, order_id):
        """Delete a single order"""
        if self.valid_request():
            order = Order.get_by_id(order_id)

            if order and order.client == self.request.headers.get('x-almanak-client-id'):
                order.key.delete()
                self.render({"message": "Ordre nr. " + order_id + " slettet"})
            else:
                self.abort(404, title="No existing order to delete")


class StructureListHandler(JsonHandler):
    def get(self):
        """Fetch the archival spaces of the current client (supplied in header)"""
        if self.valid_request():
            client = self.request.headers.get('x-almanak-client-id')
            structures = Structure.query(Structure.client == client).fetch()
            self.render(_make_serializable(structures))

    def post(self):
        """Create a new archive (eg. magasin001)"""
        if self.valid_request():
            json_body = json.loads(self.request.body.decode('utf-8'))
            label = json_body.get('label')
            structure = json_body.get('structure')

            if not label:
                self.abort(400, title="Missing label-key from request-body")
            if not structure:
                self.abort(400, title="Missing structure-key from request-body")

            for k, v in structure.items():
                if not (len(k) == 10 or k.endswith('2')):
                    self.abort(400, title='Malformed barcode in structure: ' + k)
                if not v.get('type'):
                    self.abort(400, title='Missing type-parameter in: ' + k)
                if not v.get('label'):
                    self.abort(400, title='Missing label-parameter in: ' + k)

            new_structure = Structure()
            new_structure.client = self.request.headers.get('x-almanak-client-id')
            new_structure.label = label
            new_structure.structure = structure
            new_structure.key = ndb.Key(Structure, label)
            structure_key = new_structure.put()

            self.response.set_status(201)
            self.response.headers["Location"] = ('/').join([BASE_URL, 'structures', str(structure_key.id())])
            self.render({"message": "Arkivet: " + label + " oprettet"})


class StructureItemHandler(JsonHandler):
    def get(self, structure_label):
        """Fetch the structure.json from a single archival space"""
        if self.valid_request():
            structure = Structure.get_by_id(structure_label)
            if structure and structure.client == self.request.headers.get("x-almanak-client-id"):
                # structure.structure is a JsonProperty and thus already serializable
                self.render(structure.structure)
            else:
                self.abort(404, title="Unknown structure-label")

    def put(self, structure_label):
        """Update the 'status' of a single order"""
        if self.valid_request():
            json_body = json.loads(self.request.body.decode('utf-8'))

            for k, v in json_body.items():
                if not (len(k) == 10 or k.endswith('2')):
                    self.abort(400, title='Malformed barcode in structure: ' + k)
                if not v.get('type'):
                    self.abort(400, title='Missing type-parameter in: ' + k)
                if not v.get('label'):
                    self.abort(400, title='Missing label-parameter in: ' + k)

            structure = Structure.get_by_id(structure_label)
            if not structure:
                self.abort(404, title="No structure with that id to be updated")

            structure.structure = json_body
            structure.put()
            self.render({"message": "Arkivet: " + structure_label + " updated"})

    def delete(self, structure_label):
        """Delete a single order"""
        if self.valid_request():
            structure = Structure.get_by_id(structure_label)

            if structure and structure.client == self.request.headers.get("x-almanak-client-id"):
                structure.key.delete()
                self.render({"message": "Arkivet: " + structure_label + " deleted"})
            else:
                self.abort(404, title="No such structure-label")

app = webapp2.WSGIApplication([
    # Accept only 10 digits, ending with 1, which indicates (doesn't ensure) a box-barcode
    webapp2.Route('/v1/orders/<:[0-9]{9}1>', InventoryItemHandler, methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route('/v1/orders', InventoryListHandler, methods=['GET', 'POST']),
    webapp2.Route('/v1/structures/<:[a-zA-Z0-9-_]+>', StructureItemHandler, methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route('/v1/structures', StructureListHandler, methods=['GET', 'POST'])
], debug=True)

# https://github.com/svpino/blog-engine/blob/master/main.py
# app.error_handlers[404] = JsonHandler().handle_exception(404, True)
