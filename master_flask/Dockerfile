FROM python:3.6

# Copy the python libraries needed by master_flask and install them
COPY requirements.txt ./
RUN pip install --upgrade pip \ 
    && python3 -m pip install -r requirements.txt

ARG MASTER_DOWNLOAD_FOLDER
ARG MASTER_DATA_FOLDER
ARG MASTER_RESULTS_FOLDER
ARG MASTER_PORT 

WORKDIR /
RUN mkdir ${MASTER_DOWNLOAD_FOLDER}
RUN mkdir ${MASTER_DATA_FOLDER}
RUN mkdir ${MASTER_RESULTS_FOLDER}

# Copy the master_flask app and youtube_downloader
COPY master_flask.py ./
COPY youtube_downloader.py ./
COPY video_segmenter.py ./

# Expose the port and start the wsgi
EXPOSE ${MASTER_PORT}

CMD gunicorn -b 0.0.0.0:${MASTER_PORT} master_flask
