from flask import request, make_response, Flask
from werkzeug.wrappers import WWWAuthenticateMixin
import flask
import os


api = Flask(__name__)
client = None

@api.route('/',methods=['POST'])
def create_job():
    """
    it will receive inference request on demand for anomaly service
    """
    return flask.jsonify({"satus":"200"})

    

if __name__ == '__main__':
   
    api.run(host="0.0.0.0", port=8082, debug=True)