#!/usr/bin/env python3
'''This is a module'''

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    '''handle the / route
    '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def users():
    '''Handle the /users route
    '''
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({'message': "email already registered"})
    else:
        return jsonify({'email': email, "message": 'user created'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
