from flask import Flask, request, jsonify
from functions import get_solicitudes, insert_solicitudes, get_user_info, denegar, aprobar
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        info = get_user_info(data)

    return jsonify(info)

@app.route('/get_info_user')
def get_info_user():
    return 'asd'

@app.route('/afiliacion', methods=['POST', 'GET'])
def afiliacion():
    if request.method == 'POST':
        data = request.get_json()
        data = insert_solicitudes(data)

        return jsonify(data)
    else:
        data = get_solicitudes()
        return jsonify(data)

@app.route('/options_afiliacion', methods=['PUT'])
def options_afiliacion():
    data = request.get_json()
    option = data['option']
    id = data['id']
    if option == False:
        denegar(id)
    else:
        aprobar(id)
    return jsonify(True)


if __name__ == '__main__':
    app.run()
