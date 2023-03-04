import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchema,ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return NotImplementedError("Deleting an item is not implemented.")
            
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, new_item_data, item_id):
        
        item = ItemModel.query.get_or_404(item_id)
        return NotImplementedError("Updating an item is not implemented.")


@blp.route("/items")
class ItemList(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):
        
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
            
        except SQLAlchemyError:
            abort(500, messqge="An error ocured while inserting the item.")
        
        
        
        return item