#!/bin/bash

while getopts ":i:" opt; do
    case $opt in
        i)
            INPUT_PATH=$OPTARG
            ;;
    esac
done

if [ -z "${INPUT_PATH}" ]; then
    echo "Missing input path for -i argument"
    exit 1
fi

WORKDIR=/home/dfgvi 
#    -v "${INPUT_PATH}":"${WORKDIR}/content" \
docker run \
    -it \
    --rm \
    --gpus=all \
    -v /home/james/developer/Deep-Flow-Guided-Video-Inpainting:/home/dfgvi2 \
    -v "${INPUT_PATH}":"${WORKDIR}2/content" \
    dfgvi
