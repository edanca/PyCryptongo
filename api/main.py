#
#
__author__ = 'Eduardo Cardenas'
#
#


import pymongo
from flask import Flask, jsonify, request


def get_db_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo

app = Flask(__name__)
db_connection = get_db_connection('mongodb://localhost:27017/')

def get_documents():
    # definimos parametros que vienene de la url
    params = {}
    # pedimos get y si no lo obtenemos devolvemos vacio
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))
    if name:
        params.update({ 'name' : name })
    cursor = db_connection.tickers.find(params,  { '_id' : 0, 'ticker_hash' : 0 }).limit(limit)
    return list(cursor)


def get_top20():
    params = {}
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))
    if name:
        params.update({ 'name' : name })
    params.update({ 'rank' : { '$lte' : 20 } })
    cursor = db_connection.tickers.find(params,  { '_id' : 0, 'ticker_hash' : 0 }).limit(limit)
    return list(cursor)


def remove_currency():
    #borrar tickers de una moneda
    params = {}
    name = request.args.get('name', '')
    if name:
        params.update({ 'name' : name })
    else:
        return False
    return db_connection.tickers.delete_many(params).deleted_count

@app.route("/")
def index():
    return jsonify(
        {
            'name' : 'Cryptongo API'
        }
    )


@app.route("/tickers", methods=['GET', 'DELETE'])
def tickers():
    if request.method == 'GET':
        return jsonify(get_documents())
    elif request.method == 'DELETE':
        result = remove_currency()
        if result > 0:
            return jsonify({
                'text': 'Documento se eliminó'
            }), 204
        else:
            return jsonify({
                'error': 'No se encontraron los documentos'
            }), 404



@app.route("/top20", methods=['GET'])
def top20():
    return jsonify(
        get_top20()
    )