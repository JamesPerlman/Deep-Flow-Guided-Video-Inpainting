FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

# Environment variables
ENV WORKDIR=/home/dfgvi

# ignore interactive mode, just install everything
ENV DEBIAN_FRONTEND noninteractive

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
    ffmpeg \
    wget

# Create aliases for python and pip
RUN echo "alias pip=pip3" >> ~/.bashrc && \
    echo "alias python=python3" >> ~/.bashrc

# Fetch github repo

RUN git clone https://github.com/JamesPerlman/Deep-Flow-Guided-Video-Inpainting.git ${WORKDIR}

WORKDIR ${WORKDIR}

# Install pip dependencies

RUN pip3 install -r requirements.txt

RUN pip3 install mmcv==0.2.10

# Download pretrained models

RUN pip3 install gdown

RUN gdown https://drive.google.com/drive/folders/1Nh6eJsue2IkP_bsN02SRPvWzkIi6cNbE --folder

RUN wget http://content.sniklaus.com/github/pytorch-liteflownet/network-sintel.pytorch -O pretrained_models/sintel.pth
