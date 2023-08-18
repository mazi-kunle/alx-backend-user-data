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
def logout():
    '''delete session'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    '''get user profile'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_pass():
    '''handle reset password
    '''
    email = request.form['email']
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({'email': email, 'reset_token': token})


@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''handle update password
    '''
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({'email': email, 'message': 'Password updated'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
