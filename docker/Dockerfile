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

RUN git clone https://github.com/JamesPerlman/Deep-Flow-Guided-Video-Inpainting.git ${WORKDIR} && echo cachebust commit eb3690

WORKDIR ${WORKDIR}

# Install pip dependencies

RUN pip3 install \
        addict==2.2.1 \
        certifi==2019.6.16 \
        cffi==1.12.3 \
        chardet==3.0.4 \
        cvbase==0.5.5 \
        cupy==9.6.0 \
        Cython==0.29.12 \
        idna==2.8 \
        mkl-fft \
        mkl-random \
        numpy==1.19.5 \
        olefile==0.46 \
        opencv-python==4.1.0.25 \
        Pillow==6.2.0 \
        protobuf==3.8.0 \
        pycparser==2.19 \
        PyYAML==5.1.1 \
        requests==2.22.0 \
        scipy==1.2.1 \
        six==1.12.0 \
        tensorboardX==1.8 \
        terminaltables==3.1.0 \
        torch==1.3.0 \
        torchvision==0.4.0 \
        tqdm==4.32.1 \
        urllib3==1.25.3

RUN pip3 install mmcv==0.2.10

# Download pretrained models

RUN pip3 install gdown

RUN gdown https://drive.google.com/drive/folders/1Nh6eJsue2IkP_bsN02SRPvWzkIi6cNbE --folder

RUN wget http://content.sniklaus.com/github/pytorch-liteflownet/network-sintel.pytorch -O pretrained_models/sintel.pth
