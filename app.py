from flask import Flask, request
import uuid
from flask_smorest import abort
from db import stores, items


app = Flask(__name__)

@app.get("/stores")
def GetAllStores():
    return {"Stores": list(stores.values())}


@app.get("/stores/<string:store_id>")
def GetStoreById(store_id):
    
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


@app.get("/stores/items")
def GetAllItems():
    return {"Items": list(items.values())}


@app.get("/stores/items/<string:item_id>")
def GetItemById(item_id):
    
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


@app.post("/stores")
def CreateStore():
    
    store_data = request.get_json()
    
    if (
        "name" not in store_data
        or "address" not in store_data
    ):
        print("tutaj")
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

    
@app.post("/items")
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
    
    
    
            