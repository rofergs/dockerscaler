from curses import flash
from glob import glob
from flask import Flask, json
from flask import request
import logging
import flask
import docker
import os
logging.basicConfig(level=logging.DEBUG)

root_logger = logging.getLogger()
log = root_logger

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

api = Flask(__name__)
message = "none"

@api.route('/stats', methods=['GET','POST'])
def get_stats():
    global message
    ser = client.api.services()
    for service in ser:
        if service['Spec']['Name'].find('flask-service') != -1:
            output = service
    # get replica count
    replicas = output['Spec']['Mode']['Replicated']['Replicas']
    
    return flask.jsonify({"last operation": message, "current replicas":replicas})
    
    
@api.route('/', methods=['POST'])
def scale_up():
#  print(request.get_json())
    global message
  # get alert json
    log.info("Alert received")
    try:
        alerts = request.get_json()
        #log.info(alerts)
  
    except Exception as exp:
        log.error("failed to parse data")
        return '', 500
    
  # get all services
    ser = client.api.services()
  # get service ID
    output = None
    
    # get service
    for service in ser:
        if service['Spec']['Name'].find('flask-service') != -1:
            output = service
    # get replica count
    replicas = output['Spec']['Mode']['Replicated']['Replicas']
    service_id = id = output['ID']
    serv = client.services.get(service_id)
    
    # scalling up
    if alerts['alerts'][0]['labels']['alertname'] == 'high_load':
        if replicas < int(os.environ.get("replica_limit","5")):
            serv.scale(replicas+1)
            message = "last operation was scalling up from "+ str(replicas) + " to "+ str(replicas+1)
            log.info("Successfully scaled up")
        else:
            log.info("Not scalling, limit reached")
            
    # scalling down
    if alerts['alerts'][0]['labels']['alertname'] == 'low_down':
        if replicas > 1:
            serv.scale(1)
            message = "last operation was scalling down from "+ str(replicas) + " to 1"
            log.info("Successfully scaled down")
        else:
            log.info("No need to scaled down, already 1 replica")
    return '', 200
    
if __name__ == '__main__':
    api.run(host='0.0.0.0',port=8080)