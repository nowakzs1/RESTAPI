import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store has been deleted."}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/stores")
class StoreList(MethodView):
    
    def get(self):
        return {"Stores": list(stores.values())}
    
    def post(self):
        
        store_data = request.get_json()
        
        if (
            "name" not in store_data
            or "address" not in store_data
        ):
            abort(400, message="Bad request. Ensure 'name' and 'address' is included in the JSON payload. ")
        
        for store in stores.items():
            if store_data["name"]==store["name"]:
                abort(400, message="Store already exists.")
        
        store_id = uuid.uuid4().hex
        
        new_store={
            "id":store_id,
            **store_data
        }
        
        stores[store_id]=new_store
        
        return new_store, 201