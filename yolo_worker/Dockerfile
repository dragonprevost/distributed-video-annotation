FROM alantrrs/cuda-opencv:latest

ENV BASE_DIR /darknet/darknet/

RUN mkdir /darknet
RUN mkdir /eufygg
WORKDIR /darknet
RUN git clone https://github.com/Noah-Silvera/darknet.git
WORKDIR ${BASE_DIR}
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN make OPENCV=1

ARG DARKNET_INPUT_FOLDER
ARG DARKNET_OUTPUT_FOLDER
ARG WORKER_PORT

RUN echo ${DARKNET_INPUT_FOLDER}
RUN echo ${DARKNET_OUTPUT_FOLDER}
RUN mkdir ${BASE_DIR}${DARKNET_INPUT_FOLDER}
RUN mkdir ${BASE_DIR}${DARKNET_OUTPUT_FOLDER}
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt
COPY worker_flask.py ./
COPY wsgi.py ./
ENV FLASK_APP=worker_flask.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE ${WORKER_PORT}

CMD gunicorn --bind 0.0.0.0:${WORKER_PORT} wsgi 