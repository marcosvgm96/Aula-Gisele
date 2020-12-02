# imports do código
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml
# Conecao
app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
db = client['livraria']
CORS(app)

# get
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/data', methods=['POST', 'GET'])
def data():
    # transformando o JSON em um dicionário
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

    # GET para pegar dados
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


@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):
    # métodos por id
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

    # DELETE do banco de dados
    if request.method == 'DELETE':
        db['livros'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE para atualizar os dados
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
