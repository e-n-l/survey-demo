#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS

# config

def main():
    app = connexion.App(__name__, specification_dir='./swagger/', debug=True)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Polls'}, pythonic_params=True)
    
    CORS(app.app, resources={r'/*': {'origins': '*'}})
    app.run(port=5000)


if __name__ == '__main__':
    main()
