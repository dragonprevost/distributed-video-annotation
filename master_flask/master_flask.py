from flask import Flask
from flask import request
from flask_executor import Executor
from queue import Queue
from threading import Thread
from video_segmenter import video_splitter
import requests
import logging
import urllib3
import urllib
import os
import time
import datetime

WORKER_URL = "http://%s:%d/" % (os.environ['WORKER_HOST'], int(os.environ['WORKER_PORT']))

# Debugging for requests module
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

import sys

import youtube_downloader

application = Flask(__name__)
executor = Executor(application)
FILE_LOC = os.environ['MASTER_DOWNLOAD_FOLDER']

worker_queue = Queue()

@application.route("/register", methods=["POST"])
def register():
    worker_id = request.args.get("worker_id")
    worker_queue.put(worker_id)
    _str = "Registered worker %s at %s" % (worker_id, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    print(_str, flush=True)
    return _str

@application.route("/download", methods=["POST"])
def download():
    url = request.args.get("url")
    download_thread = Thread(target=do_download_in_background, args=(url,))
    download_thread.start()
    print("Downloading %s" % (url))
    return "Downloading"


# This function is called from executor to download the video in the background
def do_download_in_background(url, loc=FILE_LOC):
    output_filename = youtube_downloader.download_video(url, loc)
    # FOR LOOP
    # segment the video in the background in a thread
    # try to pull a segment off a thread
    segment_queue = Queue()
    splitter_thread = Thread(target=video_splitter.splitVideo, args=(output_filename, segment_queue))
    splitter_thread.start()

    print("starting segment processing at %s" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    

    processed_segments = []
    while True:
        print("Waiting for segment to be available...", flush=True)
        segment = segment_queue.get()
        if not segment:
            print("No More segments", flush=True)
            # False was put onto the queue, no more segments
            break
        processed_segments.append(segment)
        worker = worker_queue.get()
        
        params = urllib.parse.urlencode({ 'filename': segment })
        print("Delegating segment %s to worker" % (segment))
        # TODO - call worker with do task PROPERLY - this is hardcoded not distributed
        worker_req_url = WORKER_URL + 'dotask/?%s' % (params)
        # print("Worker req url %s" % (worker_req_url), flush=True)
        requests.post(worker_req_url)

    # for segment in processed_segments:
    #     # ensure all segments have been output and processed
    #     while not os.path.exists(os.environ['MASTER_RESULTS_FOLDER'] + '/' + segment):
    #         time.sleep(1)
    #     print("%s analzyed" % (segment))

    print("Processed %s" % (url), flush=True)
    return


if __name__ == "__main__":
    application.run()
