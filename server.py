#!/usr/bin/python

from flask import Flask, request
from skpy import Skype as SkypeAPI
import json

app = Flask(__name__)

SKYPE_CONNECTION = None
CONFIG_FILE = 'config.json'

@app.route('/', methods=['GET'])
def default():
    return 'Please use this URL to provide to Jenkins Notification Plugin, using JSON format'

@app.route('/<api_key>', methods=['POST'])
def receive_results(api_key):
    content = {}
    # Obtain JSON data from URL
    try:
        content = json.loads(request.data)
    except:
        return {'Error': 'Data not in JSON format'}, 400

    # Load configuration file
    try:
        with open(CONFIG_FILE, 'r') as config_fh:
            config = json.loads(config_fh.read())
    except Exception as e:
        raise 'Error reading configuration file: %s' % str(e)

    if api_key not in config['APIS']:
        return 'Invalid API key', 401

    api_config = config['APIS'][api_key]
    if content['name'] in config['APIS'][api_key]['JOB_OVERRIDES']:
        build_config = config['APIS'][api_key]['JOB_OVERRIDES'][content['name']]
    else:
        build_config = {}

    return build_config

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
