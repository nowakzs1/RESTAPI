from flask import Flask, request
import uuid
from flask_smorest import abort
from db import stores, items


app = Flask(__name__)

#store functions
@app.get("/stores")
def GetAllStores():
    return {"Stores": list(stores.values())}


@app.get("/stores/<string:store_id>")
def GetStoreById(store_id):
    
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/stores")
def CreateStore():
    
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


@app.delete("/stores/<string:store_id>")
def DeleteStoreById(store_id):
    
    try:
        del stores[store_id]
        return {"message": "Store has been deleted."}
    except KeyError:
        abort(404, message="Store not found")

#item functions

@app.get("/stores/items")
def GetAllItems():
    return {"Items": list(items.values())}


@app.get("/stores/items/<string:item_id>")
def GetItemById(item_id):
    
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


@app.post("/stores/items")
def CreateItem():
    
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


@app.delete("/stores/items/<string:item_id>")
def DeleteItemById(item_id):
    
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


@app.put("/stores/items/<string:item_id>")
def UpdateAnItem(item_id): # we dont allow user to change "store_id", user can change only "name" and "price" of an item
    
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
    
            