import numpy as np
import cv2 as cv
import time
import re
import math
import sys
import os

# Constants
THRESH = 0.8
FOURCC = cv.VideoWriter_fourcc(*'MP4V')
SRCDIR = os.environ['MASTER_DOWNLOAD_FOLDER']
OUTDIR = os.environ['MASTER_DATA_FOLDER']

class VideoSegmenter():

    def __init__(self):
        self.fps = 30 # Default fps


    def splitVideo(self, filename, segment_queue):
        self.count = 0
        self.filename = filename
        self.segment_queue = segment_queue
        self.name = re.split('.mp4', self.filename)[0]
        print("Opening %s\n" % (SRCDIR + '/' + self.filename))
        self.cap = cv.VideoCapture(SRCDIR + '/' + self.filename)
        old_hist = None
        self.fps = self.cap.get(cv.CAP_PROP_FPS)

        while(self.cap.isOpened()):
            self.count = self.count + 1
             
            diff = 1
            ret, frame = self.cap.read()
            if ret==False:
                # video ended
                break
            initial_hist = cv.calcHist([frame], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
            initial_hist = cv.normalize(initial_hist, initial_hist).flatten()
            size = frame.shape[1], frame.shape[0]
            #timestamps.append(self.cap.get(cv.CAP_PROP_POS_MSEC))
            #calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
            outfile_name = self.name + str(self.count) + '.mp4'
            outfile_path = OUTDIR + '/' + outfile_name 
            segment = cv.VideoWriter(outfile_path, FOURCC, math.ceil(self.fps), size, True) 
            while(diff > THRESH):
                segment.write(frame)
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                if ret==False:
                    # video ended
                    break
                    
                hist = cv.calcHist([frame], [0, 1, 2], None, [8, 8, 8],
                                [0, 256, 0, 256, 0, 256])

                hist = cv.normalize(hist, hist).flatten()
                
                diff = cv.compareHist(initial_hist, hist, cv.HISTCMP_CORREL)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                old_hist = hist
            segment.release()
            self.segment_queue.put(outfile_name)
            print('Wrote Vid' + str(self.count) + ' ' + outfile_path, flush=True)

        # When everything done, release the capture
        self.segment_queue.put(False)
        print("Done segmenting video", flush=True)
        self.cap.release()
        cv.destroyAllWindows()


video_splitter = VideoSegmenter()
#video_splitter.splitVideo(sys.argv[1])
