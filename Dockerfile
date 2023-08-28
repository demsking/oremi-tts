ARG TENSORFLOW_VERSION
FROM tensorflow/tensorflow:${TENSORFLOW_VERSION} AS install

# Point version to master: 136877136355c82d7ba474ceb7a8f133bd84767e (Mar 10, 2022)
ARG TENSORFLOWTTS_VERSION=master

RUN apt-get update \
  && apt-get install --no-install-recommends -y cmake git

RUN pip install --no-cache-dir --upgrade pip
COPY ./setup.py.patch /tmp/setup.py.patch
RUN git clone --depth 1 --branch ${TENSORFLOWTTS_VERSION} https://github.com/TensorSpeech/TensorFlowTTS.git TensorflowTTS \
  && cd TensorflowTTS \
  && git apply /tmp/setup.py.patch \
  && pip install --no-cache-dir .

# -------------------------------------

ARG TENSORFLOW_VERSION
ARG CREATED_DATE
ARG PACKAGE_NAME
ARG MAINTAINER
ARG DOCUMENTATION
ARG DESCRIPTION
ARG VERSION
ARG SOURCE_URL
ARG VENDOR
ARG LICENSE
ARG REVISION

FROM tensorflow/tensorflow:${TENSORFLOW_VERSION}

# @see https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="$PACKAGE_NAME"
LABEL org.opencontainers.image.description="$DESCRIPTION"
LABEL org.opencontainers.image.version="$VERSION"
LABEL org.opencontainers.image.revision="$REVISION"
LABEL org.opencontainers.image.authors="$MAINTAINER"
LABEL org.opencontainers.image.created="$CREATED_DATE"
LABEL org.opencontainers.image.source="$SOURCE_URL"
LABEL org.opencontainers.image.url="$SOURCE_URL"
LABEL org.opencontainers.image.documentation="$DOCUMENTATION"
LABEL org.opencontainers.image.vendor="$VENDOR"
LABEL org.opencontainers.image.licenses="$LICENSE"
LABEL maintainer="$MAINTAINER"

RUN addgroup --system --gid 1000 oremi \
  && adduser --system --uid 1000 oremi

RUN apt-get update \
  && apt-get install --no-install-recommends -y supervisor=4.1.0-1ubuntu1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p /var/log/supervisor \
  && chown -R oremi:oremi /var/log/supervisor \
  && pip install --no-cache-dir --upgrade pip

COPY --from=install /usr/local/lib/python3.8/dist-packages /usr/local/lib/python3.8/dist-packages
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONPATH=/oremi:$PYTHONPATH
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV PATH=/oremi/bin:$PATH
ENV SERVICE_PORT=5215
ENV SERVICE_NAME=$PACKAGE_NAME

COPY ./requirements.txt /oremi/requirements.txt
RUN pip install --no-cache-dir --no-warn-script-location -r /oremi/requirements.txt \
  && pip uninstall dataclasses -y

COPY pyproject.toml LICENSE /oremi/
COPY bin/ /oremi/bin
COPY discovery/ /oremi/discovery
COPY tts/ /oremi/tts
EXPOSE 5215
USER oremi

CMD [\
  "/usr/bin/supervisord", \
    "-c", "/etc/supervisor/conf.d/supervisord.conf", \
    "-l", "/var/log/supervisor/supervisord.log" \
]
