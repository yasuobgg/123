
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

#pymongo
from pymongo import MongoClient, ReadPreference
from bson.json_util import dumps

#localmodule
from book import BOOK

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

server = os.getenv("MONGO_SERVER")
port = int(os.getenv("MONGO_PORT"))
db_name = os.getenv("MONGO_DB_NAME")
col_name = os.getenv("MONGO_COL_NAME")

client = MongoClient(server, port,
    read_preference=ReadPreference.NEAREST)
db = client.get_database(db_name)

# Error
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

# Create ( POST )
@app.route('/createbook', methods=['POST'])
def createbook():
    books = db.book
    _name = "None"
    _author = "None"
    _year = "None"
    _json=request.get_json()
    if "name" in _json:
        _name = _json['name']
    if "author" in _json:
        _author = _json['author']
    if "year" in _json:
        _year = _json['year']
    
    if _name and _author and _year:
        book1 = BOOK(_name, _author, _year)
        books.insert_one(book1.to_json())
        respone = jsonify('Book added successfully!')
        respone.status_code = 201
        return respone
    else:
        return notFound()

# Read ( GET )

# read all books
@app.route('/getbooks', methods=['GET'])
def getbooks():
    books = db.book.find()
    resp = dumps(books,indent = 6,
                         separators =(", ", " = "),
                         sort_keys = True)
    return resp

# read a book by name ( use request)
@app.route('/getabookbyname', methods=['GET'])
def getabookbyname():
    _name = request.args.get('name')
    if _name:
        book = db.book.find_one({"name":_name})
        resp = dumps(book)
        return resp
    else :
        return notFound()


#do not use request
@app.route('/getbook/<_name>', methods=['GET'])
def getabookbyname_nonrequest(_name):
    if _name:
        book = db.book.find_one({"name":_name})
        resp = dumps(book)
        return resp
    else :
        return notFound()


#read a book by id
@app.route('/getabookbyid', methods=['GET'])
def getabookbyid():
    from bson.objectid import ObjectId
    id_get = ObjectId(request.args.get('id'))
    if id_get:
        book = db.book.find_one({"_id":id_get})
        resp = dumps(book)
        return resp
    else :
        return notFound()


# Update ( PUT )
@app.route('/updateabookbyid', methods=['PUT'])
def updateabook():
    from bson.objectid import ObjectId
    id_get = ObjectId(request.args.get('id'))
    # print(id_get)
    _name = "None"
    _author = "None"
    _year = "None"
    _json=request.get_json()
    if "name" in _json:
        _name = _json['name']
    if "author" in _json:
        _author = _json['author']
    if "year" in _json:
        _year = _json['year']
    # all_id = ObjectId(db.book.find({},{"name":0,"author":0,"year":0}))
    ids = db.book.distinct('_id')
    # ids= db.book.distinct('_id', {}, {} )
    k=0
    ids_ss = dumps(id_get)
    # print(ids)
    # print(dumps(ids[0]))
    # print(ids_ss)
    for i in range(len(ids)):
        if ids_ss == dumps(ids[i]):
            k += 1
    # print(k)        
    if k==0:
        respone = jsonify('ID khong ton tai')
        return respone
    if k==1 and id_get and _name and _author and _year:
        all_updates = {
            "name": _name, 
            "author": _author,
            "year": _year
        }         
        db.book.replace_one({"_id":id_get},all_updates)
        respone = jsonify('Book updated successfully!')
        respone.status_code = 201
        return respone
    else :
        return notFound()


# Delete ( DELETE )
@app.route('/deleteabookbyid', methods=['DELETE'])
def deleteabook():
    from bson.objectid import ObjectId
    id_get = ObjectId(request.args.get('id'))

    if id_get:
        db.book.delete_one({"_id": id_get})
        respone = jsonify('Delete successfully!')
        respone.status_code = 201
        return respone
    else :
        return notFound()

if __name__ == "__main__":
    app.run(debug=True)