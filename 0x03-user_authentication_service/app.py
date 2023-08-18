#!/usr/bin/env python3
'''This is a module'''

from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    '''handle the / route
    '''
    return jsonify({'message': 'Bienvenue'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
