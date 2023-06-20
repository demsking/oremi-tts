FROM tensorflow/tensorflow:2.9.2 AS install

# Point version to master: 136877136355c82d7ba474ceb7a8f133bd84767e (Mar 10, 2022)
ARG TENSORFLOWTTS_VERSION=master

RUN apt-get update \
  && apt-get install -y cmake git

RUN pip install --upgrade pip
COPY ./setup.py.patch /tmp/setup.py.patch
RUN git clone --depth 1 --branch ${TENSORFLOWTTS_VERSION} https://github.com/TensorSpeech/TensorFlowTTS.git TensorflowTTS \
  && cd TensorflowTTS \
  && git apply /tmp/setup.py.patch \
  && pip install .

# -------------------------------------

FROM tensorflow/tensorflow:2.9.2

ENV PYTHONPATH=/var/www:$PYTHONPATH
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV TF_ENABLE_ONEDNN_OPTS=0

RUN pip install --upgrade pip
COPY --from=install /usr/local/lib/python3.8/dist-packages /usr/local/lib/python3.8/dist-packages

RUN adduser --disabled-password --gecos "" mandela
USER mandela
ENV PATH=/home/mandela/.local/bin:$PATH

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --no-warn-script-location -r /var/www/requirements.txt

COPY tts/ /var/www/tts
WORKDIR /var/www/tts
EXPOSE 5215

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5215", "server:app"]
