ARG RUNTIME_VERSION="3.8"
ARG FUNCTION_DIR="/home/app/"
ARG TORCH_DIR="/tmp"

FROM python:${RUNTIME_VERSION} AS python-alpine

RUN apt-get update && apt-get install -y cmake
RUN python${RUNTIME_VERSION} -m pip install --upgrade pip

FROM python-alpine AS build-image

ARG FUNCTION_DIR
ARG RUNTIME_VERSION
RUN mkdir -p ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}

FROM python-alpine
ARG FUNCTION_DIR
ARG TORCH_DIR
WORKDIR ${FUNCTION_DIR}

COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie

COPY entry.sh /
RUN chmod 777 /entry.sh

COPY requirements.txt ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu --target ${FUNCTION_DIR}

RUN date
ARG INCUBATOR_VER=unknown

COPY src ${FUNCTION_DIR}
RUN mkdir ${FUNCTION_DIR}/checkpoint
COPY checkpoint ${FUNCTION_DIR}/checkpoint
RUN mkdir ${TORCH_DIR}/checkpoints
COPY checkpoints ${TORCH_DIR}/checkpoints
RUN mkdir ${FUNCTION_DIR}/data
COPY data ${FUNCTION_DIR}/data
RUN rm -rf ${FUNCTION_DIR}/__pycache__
RUN mkdir ${FUNCTION_DIR}/__pycache__
COPY src/__pycache__ ${FUNCTION_DIR}/__pycache__
RUN ls -alh ${FUNCTION_DIR}/__pycache__

ENV TORCH_HOME ${TORCH_DIR}

ENTRYPOINT [ "/entry.sh" ]
CMD [ "handler.face_recognition_handler" ]