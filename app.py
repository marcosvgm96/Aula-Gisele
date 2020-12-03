# imports do código
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

#Flask
app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
db = client['livraria']
CORS(app)

@app.route('/data', methods=['POST', 'GET'])
def data():
    # POST
    if request.method == 'POST':
        body = request.json
        livro = body['livro']
        autor = body['autor']

        # inserindo as informacoes do livro no banco
        db['livros'].insert_one({
            "livro": livro,
            "autor": autor
        })
        # tranformar os dados em JSON
        return jsonify({
            'status': 'Dados Enviados',
            'livro': livro,
            'autor': autor
        })

    # GET
    if request.method == 'GET':
        allData = db['livros'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            livro = data['livro']
            autor = data['autor']
            dataDict = {
                'id': str(id),
                'livro': livro,
                'autor': autor
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

#GET por ID
@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    if request.method == 'GET':
        data = db['livros'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        livro = data['livro']
        autor = data['autor']
        dataDict = {
            'id': str(id),
            'livro': livro,
            'autor': autor
        }
        print(dataDict)
        return jsonify(dataDict)

    # DELETE
    if request.method == 'DELETE':
        db['livros'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

        # PUT
    if request.method == 'PUT':
        body = request.json
        livro = body['livro']
        autor = body['autor']

        db['livros'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "livro": livro,
                    "autor": autor
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})


if __name__ == '__main__':
    app.debug = True
    app.run()