#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    '''test register user
    '''
    url = 'http://0.0.0.0:5000/users'
    payload = {
        'email': email,
        'password': password
    }
    expected = {'email': email, "message": 'user created'}
    res = requests.post(url, data=payload)
    assert res.status_code == 200
    assert res.json() == expected


def log_in_wrong_password(email: str,
                          password: str) -> None:
    '''test login with wrong password
    '''
    url = 'http://0.0.0.0:5000/sessions'
    payload = {
        'email': email,
        'password': password
    }
    res = requests.post(url, data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    '''test login with right password
    '''
    url = 'http://0.0.0.0:5000/sessions'
    payload = {
        'email': email,
        'password': password
    }
    expected = {'email': email, 'message': 'logged in'}
    res = requests.post(url, data=payload)
    assert res.json() == expected
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    '''test profile unlogged
    '''
    url = 'http://0.0.0.0:5000/profile'
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    '''test profile logged
    '''
    url = 'http://0.0.0.0:5000/profile'
    res = requests.get(url, cookies={'session_id': session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    '''Test log out
    '''
    url = 'http://0.0.0.0:5000/sessions'
    res = requests.delete(url, cookies={'session_id': session_id})
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    '''test reset password
    '''
    url = 'http://0.0.0.0:5000/reset_password'
    res = requests.post(url, data={'email': email})
    assert res.status_code == 200
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    '''test update password
    '''
    url = 'http://0.0.0.0:5000/reset_password'
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    res = requests.put(url, data=payload)
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
