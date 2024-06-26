# memasukan library yang dibutuhkan dalam route
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin

import json

from app import app
from app.controller import UserController, ChatbotController

from flask_jwt_extended import *

api_prefix = '/api/v1/'

# route home
@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

# route register yang digunakan untuk membuat atau registrasi user
# url endpoint dari route : http://127.0.0.1:5000/register
# method post
@app.route(api_prefix + 'register', methods=['POST'])
def users():
    return UserController.register()

# route login yang digunakan untuk login user
# url endpoint dari route : http://127.0.0.1:5000/login
# method post
@app.route(api_prefix+'login', methods=['POST'])
def logins():
    return UserController.login()

# route login yang digunakan untuk login sebagai guest
# url endpoint dari route : http://127.0.0.1:5000/login-guest
# method post
@app.route(api_prefix +'login-guest', methods=['POST'])
def loginGuests():
    return UserController.loginGuest()

# route chatbot-guest digunakan untuk mengakses chatbot jika user login sebagai guest
# untuk mengakses route ini harus memerlukan token autorisasi dari user guest
# url endpoint dari route : http://127.0.0.1:5000/chatbot-guest
# method post, get
@app.route(api_prefix+'chatbot-guest', methods=['POST', 'GET'])
@jwt_required()
def botResponse():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        return ChatbotController.post_bot_response_guest(current_user)
    else:
        return ChatbotController.get_bot_response_guest(current_user)

# route chatbot-user digunakan untuk mengakses chatbot untuk user yang login
# untuk mengakses route ini harus memerlukan token autorisasi dari user yang login
# url endpoint dari route : http://127.0.0.1:5000/chatbot-user
# method post, get
@app.route(api_prefix+'chatbot-user', methods=['POST', 'GET'])
@jwt_required()
def botUserResponse():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        return ChatbotController.post_bot_response_user(current_user)
    else:
        return ChatbotController.get_bot_response_user(current_user)

# route logout digunakan untuk melakukan logout dari aplikasi untuk user yang login maupun guest
# untuk mengakses route ini harus memerlukan token autorisasi dari user atau guest
# url endpoint dari route : http://127.0.0.1:5000/logout
# method delete
@app.route(api_prefix+"logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    current_user = get_jwt_identity()
    return UserController.modify_token(current_user)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

