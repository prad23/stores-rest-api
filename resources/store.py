from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_id',type=int,required=True,help="This cannot be left blank.")
    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An item with name '{}' already exsits.".format(name)}, 400
        
        data = Store.parser.parse_args()

        store = StoreModel(name)
        try:
            store.upsert()
        except:
            return {'message':'An error occurred.'}, 500 # Internal server error
        return store.json(), 201

    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

