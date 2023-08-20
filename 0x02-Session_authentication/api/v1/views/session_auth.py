#!/usr/bin/env python3
'''Module of Sesson views
'''
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def auth_session():
    '''handle auth session
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if (email is None):
        return jsonify({'error': 'email missing'}), 400
    elif password is None:
        return jsonify({'error': 'password missing'}), 400

    User()
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        import os

        session_id = auth.create_session(user[0].id)
        resp = make_response(user[0].to_json())
        resp.set_cookie(os.getenv('SESSION_NAME'), session_id)

        return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    '''handle logout
    '''
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({})
    else:
        abort(404)
