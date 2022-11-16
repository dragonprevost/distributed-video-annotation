import flask
import subprocess
from threading import Thread
import shutil
import os
import sys
import requests
import logging
import urllib3

#debugging for requests module
# try: # for Python 3
#     from http.client import HTTPConnection
# except ImportError:
#     from httplib import HTTPConnection
# HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

application = flask.Flask(__name__)

MASTER_URL = "http://%s:%d/" % (os.environ['MASTER_HOST'], int(os.environ['MASTER_PORT']))

YOLO_CMD = ['./darknet','detector', 'demo', 'cfg/coco.data', 'cfg/yolov3.cfg', 'yolov3.weights','']
BASE_DIR = os.environ['BASE_DIR']
FILE_LOC = BASE_DIR + os.environ['DARKNET_INPUT_FOLDER']
RESULTS_LOC = BASE_DIR + os.environ['DARKNET_OUTPUT_FOLDER']

# TODO - this needs to be an env variable, probably a workers internal IP
worker_id = 1

def register():
  print("Registering with master", flush=True)
  requests.post(MASTER_URL + "register?worker_id=%s" % (worker_id))

def process_file(filename):
  yoloThread = Thread(target=yolo, args=(filename,))
  yoloThread.start()

def yolo(filename):
    file_path = (FILE_LOC + '/' + filename)
    print("Processing %s" % file_path, flush=True)    
    YOLO_CMD[-1] = file_path   
    print(YOLO_CMD, flush=True)
    subprocess.run(YOLO_CMD)
    print("Finished processing file", flush=True)
    # send a response back to master now
    # os.chdir(BASE_DIR)
    # renFolder= os.environ['DARKNET_OUTPUT_FOLDER']
    # # TODO - this needs to be parameteritzed
    # oldname = 'predictions.jpg'
    # newname= filename
    # shutil.move(oldname, renFolder+'/'+newname)
    register()
    


def handle(filename):
    process_file(filename)

@application.route('/dotask/', methods=['POST'])
def do_task():
    req = flask.request
    filename = req.args.get('filename')
    print("Received Task to process file %s" % (filename), flush=True)
    handle(filename)
    return "Processing %s" % (filename)

register()

if __name__ == "__main__":
    application.run()