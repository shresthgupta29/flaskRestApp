from flask_restful import Resource
from models.storeModel import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'msg' : 'Store not found'}, 404
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'msg' : "A store with name {} alredy exists".format(name)},400
        store = StoreModel(name)
        try:
            store.add_to_db()
        except:
            return {'msg' : "An error occured while adding store to db"},500

        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'msg' : 'Store deleted'},200

class StoreList(Resource):
    def get(self):
        #return {'stores' : store.json() for store in StoreModel.query.all()}
        return {'stores' : list(map(lambda store : store.json(), StoreModel.query.all()))}