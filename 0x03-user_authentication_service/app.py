#!/usr/bin/env python3
'''This is a module'''

from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['POST'])
def sessions():
    '''Handle /sessions route
    '''
    email = request.form['email']
    password = request.form['password']
    # login validation
    if AUTH.valid_login(email, password):
        new_session = AUTH.create_session(email)
        resp = jsonify({'email': email, 'message': 'logged in'})
        resp.set_cookie('session_id', new_session)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def delSession():
    '''delete session'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
