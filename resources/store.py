import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return NotImplementedError("Deleting an store is not implemented.")


@blp.route("/stores")
class StoreList(MethodView):
    
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        
        new_store = StoreModel(**store_data)
        
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message = "A store with taht name already exist."
            )
        except SQLAlchemyError:
            abort(
                500,
                message = "An error ocured while creating a store."
            )
        
        return new_store