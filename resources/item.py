from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.itemModel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be blank")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json() , 200
        return {'msg' : "item not found"} , 404




    def post(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            return {'msg': "item with name {} already exits".format(name)},400
        item =  ItemModel(name,**data)
        try:
            item.insert()
        except:
            return {'msg' : 'An error occured while inserting'}, 500 #internal server error

        return item.json() , 201 #created              #202 okay  #404 Not Found #202 Accepted

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
        return {'msg' : 'item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item :
            item.price= data['price']
        else:
            item = ItemModel(name,**data)
        item.insert()
        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}
        #return {'items' : list(map(lambda x : x.json(), ItemModel.query.all()))}