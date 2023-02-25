import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from db import stores


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    
    def get(self, item_id):
        
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")
            
    def put(self, item_id):
        
        new_item_data = request.get_json()
        
        if(
            "name" not in new_item_data
            or "price" not in new_item_data
        ):
            abort(400, message="Bad request. Ensure that 'name' or 'price' are included in the JSON payload.")
        
        try:
            item = items[item_id]
            item |= new_item_data
            
            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/items")
class ItemList(MethodView):
    
    def get(self):
        return {"Items": list(items.values())}
    
    def post(self):
        item_data=request.get_json()
    
    
        if (
            "store_id" not in item_data
            or "price" not in item_data
            or "name" not in item_data
        ):
            abort(400, message="Bad request. Ensure 'store_id', 'name' and 'price' is included in the JSON payload.")
            
        if item_data["store_id"] not in stores:
            abort(400, message="Store not found. Ensure 'store_id' value is entered correctly.")
        
        for item in items.values():
            if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
            ): 
                abort(400, message="Item already exists.")
        
        
        item_id= uuid.uuid4().hex
        new_item={
            "item_id": item_id,
            **item_data
        }
        
        items[item_id]=new_item
        return new_item, 201