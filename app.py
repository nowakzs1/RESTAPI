import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_migrate import Migrate

from db import db
import models


from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True 
    # Jesli jest jakis wyjatek poza naszym app to zebysmy mogli go widziec

    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    #Standard dokumentacji
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # mowi flask smorest ze ma uzywac swaggera 
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # kod do pobrania zeby zrobic to co wyzej linijke
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    
    #podlaczenie sql alchemy do app, wiele prowajderow ma connection linka dal clienta, z racji ze my mamy database w cliencie to mamy link:
    #sqlite:///data.db
    # korzystamy wiec z sqlite, mozemy tez skorzystac z postgres ale to inny link by byl
    # the way we acces environment variable is os.getenv("DATABASE_URL", LINK)
    # czyli jesli mamy database url to zaimportuje sobie, jesli nie to uzyje defaultowego czyli to co wpiszemy w miejscu LINK
    #musimy wiec zaimportowac os
    # "DATABESE_URL" -  importujemy tak bazy danych bo pozniej jak sherujemy kod to nie chcemy zeby ktos znal nasza baze danych 
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # malo wazne, juz sie chyba nie uzywa
    db.init_app(app)
    # inicjalizuje rozszerzenie flask sql alchemy i daje app aby mogl je połączyć

    migrate = Migrate(app, db)
    
    api = Api(app) # connects flask smortest extensions to the flask app
    
    
    app.config["JWT_SECRET_KEY"] = "82955507359750837915888689411803118775"
    jwt = JWTManager(app)
    
    #with app.app_context(): # zanim wykonamy operacje na tabelach tworzymy ja, jesli nie ma juz stworzonych tabeli
    #    db.create_all() # wie co stworzyc bo ma zaimportowane models
    
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    #if above function return True(if users token is terminated) this function return error for user
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

     
    # zamiast tego with mozemy uzyc tego:   
    #@app.before_first_request
    #def create_tables():
    #    db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    return app
