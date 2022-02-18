FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

# Environment variables
ENV WORKDIR=/home/dfgvi

# Install apt dependencies

RUN apt update -y && \
    apt install -y \
    python3 \
    python3-pip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    ffmpeg

# Fetch github repo

RUN git clone https://github.com/JamesPerlman/Deep-Flow-Guided-Video-Inpainting.git ${WORKDIR} && echo cachebust bded92

WORKDIR ${WORKDIR}

# Install pip dependencies

RUN pip3 install -r requirements.txt

RUN bash install_scripts.sh

# Download pretrained models

RUN pip3 install gdown

RUN gdown https://drive.google.com/drive/folders/1Nh6eJsue2IkP_bsN02SRPvWzkIi6cNbE --folder
